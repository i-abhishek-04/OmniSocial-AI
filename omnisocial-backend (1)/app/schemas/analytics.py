"""
Pydantic response models for analytics endpoints.
"""
from pydantic import BaseModel


class PlatformSummary(BaseModel):
    platform: str
    display_name: str
    connected: bool
    handle: str
    followers: int
    engagement_rate: float
    avg_views: int
    posts_count: int
    growth_30d: float
    monthly_revenue: float
    color: str
    is_live: bool
    is_supported: bool
    coming_soon_message: str | None = None


class OverviewResponse(BaseModel):
    total_followers: int
    total_engagement_rate: float
    total_monthly_revenue: float
    avg_growth_30d: float
    connected_platforms: int
    total_platforms: int
    supported_platforms: int
    coming_soon_platforms: int
    platforms: list[PlatformSummary]
    follower_trend: list[dict]
    top_platform: str | None


class TimeseriesPoint(BaseModel):
    date: str
    followers: int
    views: int
    engagement_rate: float


class PlatformDetailResponse(BaseModel):
    platform: str
    display_name: str
    connected: bool
    handle: str
    followers: int
    engagement_rate: float
    avg_views: int
    posts_count: int
    growth_30d: float
    monthly_revenue: float
    color: str
    is_live: bool
    is_supported: bool
    coming_soon_message: str | None = None
    timeseries: list[TimeseriesPoint]


class RevenueByPlatform(BaseModel):
    platform: str
    display_name: str
    amount: float
    color: str


class RevenueMonth(BaseModel):
    month: str
    total: float
    by_platform: list[RevenueByPlatform]


class RevenueResponse(BaseModel):
    total_this_month: float
    total_last_month: float
    change_pct: float
    months: list[RevenueMonth]
    breakdown_this_month: list[RevenueByPlatform]


class ConnectPlatformRequest(BaseModel):
    handle: str
