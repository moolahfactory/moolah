from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter()


@router.post("/budgets/", response_model=schemas.Budget)
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.create_budget(db, budget, user_id=current_user.id)


@router.get("/budgets/", response_model=list[schemas.Budget])
def read_budgets(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.get_budgets(db, user_id=current_user.id)


@router.put("/budgets/{budget_id}", response_model=schemas.Budget)
def update_budget(
    budget_id: int,
    budget: schemas.BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.update_budget(db, budget_id, budget, user_id=current_user.id)


@router.delete("/budgets/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    crud.delete_budget(db, budget_id, user_id=current_user.id)
    return {"detail": "Budget deleted"}

