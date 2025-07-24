from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter()


@router.get("/summary/monthly", response_model=list[schemas.MonthlySummary])
def monthly_summary(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    results = crud.get_summary(db, user_id=current_user.id, group_by_month=True)
    return [schemas.MonthlySummary(month=r.month, total=r.total) for r in results]


@router.get("/summary/category", response_model=list[schemas.CategorySummary])
def category_summary(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    results = crud.get_summary(db, user_id=current_user.id, group_by_category=True)
    return [
        schemas.CategorySummary(category=r.category or "Uncategorized", total=r.total)
        for r in results
    ]
