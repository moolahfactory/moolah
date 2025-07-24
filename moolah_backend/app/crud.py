from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from decimal import Decimal
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import logging
import os

from . import models, schemas

SECRET_KEY = os.getenv("MOOLAH_SECRET_KEY")
if not SECRET_KEY:
    message = "Environment variable MOOLAH_SECRET_KEY must be set"
    logging.error(message)
    raise RuntimeError(message)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Points required to reach each level
LEVEL_THRESHOLDS = [
    ("Bronze", 100),
    ("Silver", 500),
    ("Gold", 1000),
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def _check_and_create_rewards(db: Session, user: models.User):
    existing = {reward.level for reward in user.rewards}
    for level, points_required in LEVEL_THRESHOLDS:
        if user.points >= points_required and level not in existing:
            reward = models.Reward(level=level, points=user.points, owner_id=user.id)
            db.add(reward)


def create_transaction(
    db: Session,
    transaction: schemas.TransactionCreate,
    user_id: int,
    *,
    timestamp: datetime | None = None,
):
    ts = timestamp or datetime.utcnow()
    db_tx = models.Transaction(
        **transaction.model_dump(), owner_id=user_id, timestamp=ts
    )
    user = db.get(models.User, user_id)

    month_key = db_tx.timestamp.strftime("%Y-%m")
    budget = (
        db.query(models.Budget)
        .filter(models.Budget.owner_id == user_id, models.Budget.month == month_key)
        .first()
    )
    if budget and db_tx.amount < 0:
        dialect = db.bind.dialect.name
        if dialect == "sqlite":
            month_expr = func.strftime("%Y-%m", models.Transaction.timestamp)
        else:
            month_expr = func.to_char(
                func.date_trunc("month", models.Transaction.timestamp),
                "YYYY-MM",
            )

        spent = (
            db.query(func.sum(models.Transaction.amount))
            .filter(
                models.Transaction.owner_id == user_id,
                month_expr == month_key,
                models.Transaction.amount < 0,
            )
            .scalar()
            or Decimal("0")
        )
        spent = abs(spent) + abs(db_tx.amount)
        if spent > budget.limit:
            raise HTTPException(status_code=400, detail="Budget exceeded")

    db.add(db_tx)
    # Gamification: earn points for each transaction
    user.points += int(abs(db_tx.amount))

    _check_and_create_rewards(db, user)

    db.commit()
    db.refresh(db_tx)
    db.refresh(user)

    return db_tx


def get_transactions(
    db: Session,
    user_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    category_id: int | None = None,
):
    query = db.query(models.Transaction).filter(models.Transaction.owner_id == user_id)
    if start_date:
        query = query.filter(models.Transaction.timestamp >= start_date)
    if end_date:
        query = query.filter(models.Transaction.timestamp <= end_date)
    if category_id:
        query = query.filter(models.Transaction.category_id == category_id)
    return query.all()


def update_transaction(
    db: Session,
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    user_id: int,
):
    db_tx = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == user_id,
        )
        .first()
    )
    if not db_tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    user = db.get(models.User, user_id)

    old_amount = db_tx.amount
    for key, value in transaction.model_dump(exclude_unset=True).items():
        setattr(db_tx, key, value)

    month_key = db_tx.timestamp.strftime("%Y-%m")
    budget = (
        db.query(models.Budget)
        .filter(models.Budget.owner_id == user_id, models.Budget.month == month_key)
        .first()
    )
    if budget and db_tx.amount < 0:
        dialect = db.bind.dialect.name
        if dialect == "sqlite":
            month_expr = func.strftime("%Y-%m", models.Transaction.timestamp)
        else:
            month_expr = func.to_char(
                func.date_trunc("month", models.Transaction.timestamp),
                "YYYY-MM",
            )

        spent = (
            db.query(func.sum(models.Transaction.amount))
            .filter(
                models.Transaction.owner_id == user_id,
                month_expr == month_key,
                models.Transaction.amount < 0,
                models.Transaction.id != db_tx.id,
            )
            .scalar()
            or Decimal("0")
        )
        spent = abs(spent) + abs(db_tx.amount)
        if spent > budget.limit:
            db.rollback()
            raise HTTPException(status_code=400, detail="Budget exceeded")

    user.points -= int(abs(old_amount))
    user.points += int(abs(db_tx.amount))

    _check_and_create_rewards(db, user)

    db.commit()
    db.refresh(db_tx)
    db.refresh(user)

    return db_tx


def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_tx = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == user_id,
        )
        .first()
    )
    if not db_tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_tx)
    db.commit()


def create_goal(db: Session, goal: schemas.GoalCreate, user_id: int):
    db_goal = models.Goal(**goal.model_dump(), owner_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def get_goals(db: Session, user_id: int):
    return db.query(models.Goal).filter(models.Goal.owner_id == user_id).all()


def update_goal(db: Session, goal_id: int, goal: schemas.GoalUpdate, user_id: int):
    db_goal = (
        db.query(models.Goal)
        .filter(models.Goal.id == goal_id, models.Goal.owner_id == user_id)
        .first()
    )
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in goal.model_dump(exclude_unset=True).items():
        setattr(db_goal, key, value)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def set_goal_achieved(db: Session, goal_id: int, user_id: int):
    db_goal = (
        db.query(models.Goal)
        .filter(models.Goal.id == goal_id, models.Goal.owner_id == user_id)
        .first()
    )
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    user = db.get(models.User, user_id)
    if not db_goal.achieved:
        db_goal.achieved = True
        user.points += int(db_goal.target_amount)

    _check_and_create_rewards(db, user)

    db.commit()
    db.refresh(db_goal)
    db.refresh(user)

    return db_goal, user


def delete_goal(db: Session, goal_id: int, user_id: int):
    db_goal = (
        db.query(models.Goal)
        .filter(models.Goal.id == goal_id, models.Goal.owner_id == user_id)
        .first()
    )
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(db_goal)
    db.commit()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
    db.refresh(db_category)
    return db_category


def get_categories(db: Session):
    return db.query(models.Category).all()


def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_cat = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_cat, key, value)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def delete_category(db: Session, category_id: int):
    db_cat = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_cat)
    db.commit()


def create_budget(db: Session, budget: schemas.BudgetCreate, user_id: int):
    db_budget = models.Budget(**budget.model_dump(), owner_id=user_id)
    db.add(db_budget)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Budget already exists")
    db.refresh(db_budget)
    return db_budget


def get_budgets(db: Session, user_id: int):
    return db.query(models.Budget).filter(models.Budget.owner_id == user_id).all()


def update_budget(
    db: Session, budget_id: int, budget: schemas.BudgetUpdate, user_id: int
):
    db_budget = (
        db.query(models.Budget)
        .filter(models.Budget.id == budget_id, models.Budget.owner_id == user_id)
        .first()
    )
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    for key, value in budget.model_dump(exclude_unset=True).items():
        setattr(db_budget, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Budget already exists")
    db.refresh(db_budget)
    return db_budget


def delete_budget(db: Session, budget_id: int, user_id: int):
    db_budget = (
        db.query(models.Budget)
        .filter(models.Budget.id == budget_id, models.Budget.owner_id == user_id)
        .first()
    )
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(db_budget)
    db.commit()


def get_rewards(db: Session, user_id: int):
    return db.query(models.Reward).filter(models.Reward.owner_id == user_id).all()


def get_summary(
    db: Session,
    user_id: int,
    group_by_month: bool = False,
    group_by_category: bool = False,
):
    query = db.query(func.sum(models.Transaction.amount).label("total"))

    group_fields = []

    if group_by_category:
        category_col = models.Category.name
        query = query.add_columns(category_col.label("category")).join(
            models.Category,
            models.Transaction.category_id == models.Category.id,
            isouter=True,
        )
        group_fields.append(category_col)

    if group_by_month:
        dialect = db.bind.dialect.name
        if dialect == "sqlite":
            month_expr = func.strftime("%Y-%m", models.Transaction.timestamp)
        else:
            month_expr = func.to_char(
                func.date_trunc("month", models.Transaction.timestamp),
                "YYYY-MM",
            )
        query = query.add_columns(month_expr.label("month"))
        group_fields.append(month_expr)

    query = query.filter(models.Transaction.owner_id == user_id)

    if group_fields:
        query = query.group_by(*group_fields)
    return query.all()


def create_whatsapp_message(db: Session, message: schemas.WhatsAppMessageCreate):
    db_msg = models.WhatsAppMessage(
        wa_id=message.wa_id,
        from_number=message.from_number,
        body=message.body,
        timestamp=message.timestamp,
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


def get_whatsapp_messages(db: Session):
    return db.query(models.WhatsAppMessage).all()
