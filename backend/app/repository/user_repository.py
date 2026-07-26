"""
User persistence.
"""
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create(db: Session, *, email: str, full_name: str, hashed_password: str, niche: str) -> User:
    user = User(email=email, full_name=full_name, hashed_password=hashed_password, niche=niche)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, **fields) -> User:
    for key, value in fields.items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
