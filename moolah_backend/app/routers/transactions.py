from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from .. import crud, schemas
from ..dependencies import get_current_user
from ..database import get_db

router = APIRouter()


@router.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.create_transaction(db, transaction, user_id=current_user.id)


@router.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.get_transactions(
        db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
    )


@router.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.update_transaction(db, transaction_id, transaction, user_id=current_user.id)


@router.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    crud.delete_transaction(db, transaction_id, user_id=current_user.id)
    return {"detail": "Transaction deleted"}
