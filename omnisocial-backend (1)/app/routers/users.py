"""
User routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.repository import user_repository
from app.schemas.user import UserUpdateRequest, UserResponse
from app.utils.helpers import success_response

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return success_response(UserResponse.model_validate(current_user).model_dump(mode="json"))


@router.put("/me")
def update_me(
    payload: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = user_repository.update(db, current_user, full_name=payload.full_name, niche=payload.niche)
    return success_response(UserResponse.model_validate(updated).model_dump(mode="json"), "Profile updated")
