from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, String, Text, DateTime
from app.core.database import Base


class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    platforms = Column(String, nullable=False)  # Comma-separated platform IDs e.g. "youtube,github"
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="scheduled")  # "draft", "scheduled", "published"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "platforms": [p.strip() for p in self.platforms.split(",") if p.strip()],
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
