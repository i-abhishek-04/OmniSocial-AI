"""
Authentication routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserCreateRequest, LoginRequest, TokenResponse, UserResponse
from app.services import auth_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: UserCreateRequest, db: Session = Depends(get_db)):
    user, token = auth_service.register(
        db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        niche=payload.niche,
    )
    data = TokenResponse(access_token=token, user=UserResponse.model_validate(user))
    return success_response(data.model_dump(mode="json"), "Account created")


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user, token = auth_service.login(db, email=payload.email, password=payload.password)
    data = TokenResponse(access_token=token, user=UserResponse.model_validate(user))
    return success_response(data.model_dump(mode="json"), "Logged in")


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return success_response(UserResponse.model_validate(current_user).model_dump(mode="json"))
