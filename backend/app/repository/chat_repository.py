"""
Chat message persistence.
"""
from sqlalchemy.orm import Session

from app.models.chat import ChatMessage


def add_message(db: Session, *, user_id: str, role: str, content: str) -> ChatMessage:
    msg = ChatMessage(user_id=user_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_history(db: Session, user_id: str, limit: int = 50) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.created_at.asc())
        .limit(limit)
        .all()
    )
