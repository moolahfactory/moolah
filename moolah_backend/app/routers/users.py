from fastapi import APIRouter, Depends
from .. import schemas
from ..dependencies import get_current_user

router = APIRouter()


@router.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user
