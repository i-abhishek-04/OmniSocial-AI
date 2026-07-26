from pydantic import BaseModel, Field


class ScheduledPostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    platforms: list[str] = Field(..., min_items=1)
    scheduled_at: str  # ISO string
    status: str = "scheduled"


class ScheduledPostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    platforms: list[str] | None = None
    scheduled_at: str | None = None
    status: str | None = None
