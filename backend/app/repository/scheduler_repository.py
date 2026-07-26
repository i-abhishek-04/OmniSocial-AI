from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.scheduled_post import ScheduledPost


def get_posts_for_user(db: Session, user_id: str) -> list[ScheduledPost]:
    return (
        db.query(ScheduledPost)
        .filter(ScheduledPost.user_id == user_id)
        .order_by(ScheduledPost.scheduled_at.asc())
        .all()
    )


def create_post(
    db: Session,
    user_id: str,
    title: str,
    content: str,
    platforms: list[str],
    scheduled_at: datetime,
    status: str = "scheduled",
) -> ScheduledPost:
    post = ScheduledPost(
        user_id=user_id,
        title=title,
        content=content,
        platforms=",".join(platforms),
        scheduled_at=scheduled_at,
        status=status,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post_by_id(db: Session, user_id: str, post_id: str) -> ScheduledPost | None:
    return (
        db.query(ScheduledPost)
        .filter(ScheduledPost.user_id == user_id, ScheduledPost.id == post_id)
        .first()
    )


def update_post(
    db: Session,
    post: ScheduledPost,
    title: str | None = None,
    content: str | None = None,
    platforms: list[str] | None = None,
    scheduled_at: datetime | None = None,
    status: str | None = None,
) -> ScheduledPost:
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content
    if platforms is not None:
        post.platforms = ",".join(platforms)
    if scheduled_at is not None:
        post.scheduled_at = scheduled_at
    if status is not None:
        post.status = status

    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: ScheduledPost) -> bool:
    db.delete(post)
    db.commit()
    return True
