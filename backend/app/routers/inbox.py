from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.services import inbox_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/inbox", tags=["inbox"])


@router.get("/messages")
async def get_messages(
    platform: str | None = Query(None),
    unread_only: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    messages = await inbox_service.get_inbox_messages(db, current_user.id, platform=platform, unread_only=unread_only)
    return success_response(messages)
