"""
Chat routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.repository import chat_repository
from app.schemas.chat import ChatMessageRequest, ChatMessageItem
from app.services import chat_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/messages")
async def send_message(
    payload: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reply = await chat_service.send_message(db, current_user.id, current_user.email, payload.message)
    return success_response({"reply": ChatMessageItem.model_validate(reply).model_dump(mode="json")})


@router.get("/history")
def history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    messages = chat_repository.get_history(db, current_user.id)
    return success_response({
        "messages": [ChatMessageItem.model_validate(m).model_dump(mode="json") for m in messages]
    })
