from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_current_user
from ..database import get_db

router = APIRouter()


@router.post("/goals/", response_model=schemas.Goal)
def create_goal(
    goal: schemas.GoalCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.create_goal(db, goal, user_id=current_user.id)


@router.get("/goals/", response_model=list[schemas.Goal])
def read_goals(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.get_goals(db, user_id=current_user.id)


@router.put("/goals/{goal_id}", response_model=schemas.Goal)
def update_goal(
    goal_id: int,
    goal: schemas.GoalUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.update_goal(db, goal_id, goal, user_id=current_user.id)


@router.patch("/goals/{goal_id}/complete", response_model=schemas.UserProgress)
def complete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    crud_goal, user = crud.set_goal_achieved(db, goal_id, user_id=current_user.id)
    rewards = crud.get_rewards(db, user_id=current_user.id)
    return schemas.UserProgress(points=user.points, rewards=rewards)


@router.delete("/goals/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    crud.delete_goal(db, goal_id, user_id=current_user.id)
    return {"detail": "Goal deleted"}
