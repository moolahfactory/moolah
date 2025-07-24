from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_current_user
from ..database import get_db

router = APIRouter()


@router.get("/rewards/", response_model=schemas.UserProgress)
def read_rewards(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    rewards = crud.get_rewards(db, user_id=current_user.id)
    return schemas.UserProgress(points=current_user.points, rewards=rewards)
