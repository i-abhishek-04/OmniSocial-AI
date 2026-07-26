"""
SocialAccount ORM model.

Stores the current "snapshot" stats for each supported platform, per user
- both the fully-functional ones (real public APIs) and the "Coming Soon"
placeholders, so every platform has a row and the dashboard always has
something to render. Historical/time-series and revenue figures are
derived on the fly (deterministically, seeded per account) by
services/analytics_service.py rather than stored row-by-row - this keeps
the schema light. See services/platforms/registry.py for the single
source of truth on which platforms exist and which are live.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.services.platforms.registry import ALL_PLATFORM_IDS

# Kept as SUPPORTED_PLATFORMS (rather than renaming every import site) -
# it now means "every platform with a dashboard row", live or coming-soon.
# Order matches registry.py: live platforms first, then coming-soon.
SUPPORTED_PLATFORMS = ALL_PLATFORM_IDS


def _uuid() -> str:
    return str(uuid.uuid4())


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)

    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    handle: Mapped[str] = mapped_column(String(100), nullable=False)
    connected: Mapped[bool] = mapped_column(Boolean, default=False)

    followers: Mapped[int] = mapped_column(Integer, default=0)
    engagement_rate: Mapped[float] = mapped_column(Float, default=0.0)
    avg_views: Mapped[int] = mapped_column(Integer, default=0)
    posts_count: Mapped[int] = mapped_column(Integer, default=0)
    growth_30d: Mapped[float] = mapped_column(Float, default=0.0)
    is_live: Mapped[bool] = mapped_column(Boolean, default=False)

    connected_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="social_accounts")
