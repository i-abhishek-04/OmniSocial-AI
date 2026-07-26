from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.scheduler import ScheduledPostCreate, ScheduledPostUpdate
from app.services import scheduler_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


@router.get("/posts")
def get_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    posts = scheduler_service.list_posts(db, current_user.id)
    return success_response(posts)


@router.post("/posts")
def create_post(
    payload: ScheduledPostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = scheduler_service.create_post(
        db,
        user_id=current_user.id,
        title=payload.title,
        content=payload.content,
        platforms=payload.platforms,
        scheduled_at_iso=payload.scheduled_at,
        status=payload.status,
    )
    return success_response(post, "Post scheduled successfully")


@router.put("/posts/{post_id}")
def update_post(
    post_id: str,
    payload: ScheduledPostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated = scheduler_service.update_post(
        db,
        user_id=current_user.id,
        post_id=post_id,
        title=payload.title,
        content=payload.content,
        platforms=payload.platforms,
        scheduled_at_iso=payload.scheduled_at,
        status=payload.status,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Scheduled post not found")
    return success_response(updated, "Post updated successfully")


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    success = scheduler_service.delete_post(db, current_user.id, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Scheduled post not found")
    return success_response({"id": post_id}, "Post deleted successfully")


@router.get("/recommendations")
async def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recs = await scheduler_service.get_best_time_recommendations(db, current_user.id, current_user.email)
    return success_response(recs)
