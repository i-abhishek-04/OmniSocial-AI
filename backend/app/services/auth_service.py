"""
Auth business logic: registration and login orchestration.
"""
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.repository import user_repository
from app.utils.exceptions import ConflictError, UnauthorizedError


def register(db: Session, *, email: str, password: str, full_name: str, niche: str) -> tuple[User, str]:
    if user_repository.get_by_email(db, email):
        raise ConflictError("An account with this email already exists")
    user = user_repository.create(
        db, email=email, full_name=full_name, hashed_password=hash_password(password), niche=niche
    )
    token = create_access_token(subject=user.id)
    return user, token


def login(db: Session, *, email: str, password: str) -> tuple[User, str]:
    user = user_repository.get_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedError("Invalid email or password")
    token = create_access_token(subject=user.id)
    return user, token
