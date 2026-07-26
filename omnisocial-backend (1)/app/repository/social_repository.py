"""
SocialAccount persistence.
"""
from sqlalchemy.orm import Session

from app.models.social_account import SocialAccount, SUPPORTED_PLATFORMS


def get_all_for_user(db: Session, user_id: str) -> list[SocialAccount]:
    return db.query(SocialAccount).filter(SocialAccount.user_id == user_id).all()


def get_platform_for_user(db: Session, user_id: str, platform: str) -> SocialAccount | None:
    return (
        db.query(SocialAccount)
        .filter(SocialAccount.user_id == user_id, SocialAccount.platform == platform)
        .first()
    )


def set_connected(db: Session, account: SocialAccount, connected: bool, handle: str | None = None) -> SocialAccount:
    account.connected = connected
    if handle:
        account.handle = handle
    db.commit()
    db.refresh(account)
    return account


def update_live_stats(
    db: Session,
    account: SocialAccount,
    *,
    followers: int,
    posts_count: int,
    avg_views: int,
) -> SocialAccount:
    """Overwrite an account's snapshot with real data fetched from a live
    platform API (see services/youtube_service.py), marking it is_live so
    the frontend can show a "Live" badge instead of "Demo"."""
    account.followers = followers
    account.posts_count = posts_count
    account.avg_views = avg_views
    account.is_live = True
    db.commit()
    db.refresh(account)
    return account


def ensure_seeded(db: Session, user_id: str, user_email: str) -> list[SocialAccount]:
    """Create a snapshot row for every supported platform the first time a
    user is seen, so /analytics endpoints always have something to read.
    Uses deterministic-but-varied demo numbers derived from the platform
    name; see services/analytics_service.py for the generation logic."""
    from app.services.analytics_service import generate_snapshot_stats

    existing = {a.platform for a in get_all_for_user(db, user_id)}
    created = []
    for platform in SUPPORTED_PLATFORMS:
        if platform in existing:
            continue
        stats = generate_snapshot_stats(user_id, platform)
        account = SocialAccount(
            user_id=user_id,
            platform=platform,
            handle="@" + user_email.split("@")[0],
            connected=stats["connected"],
            followers=stats["followers"],
            engagement_rate=stats["engagement_rate"],
            avg_views=stats["avg_views"],
            posts_count=stats["posts_count"],
            growth_30d=stats["growth_30d"],
        )
        db.add(account)
        created.append(account)
    if created:
        db.commit()
        for a in created:
            db.refresh(a)
    return get_all_for_user(db, user_id)
