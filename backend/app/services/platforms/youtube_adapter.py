"""
YouTube adapter - thin wrapper around services/youtube_service.py (the
existing, unmodified YouTube Data API v3 integration) so it speaks the
common PlatformAdapter contract.
"""
from app.services import youtube_service
from app.services.platforms.base import PlatformAdapter, PublicStats


class YouTubeAdapter(PlatformAdapter):
    platform_id = "youtube"
    display_name = "YouTube"
    color = "#FF0000"
    is_live = True

    async def fetch_public_stats(self, handle: str) -> PublicStats | None:
        stats = await youtube_service.fetch_channel_stats(handle)
        if not stats:
            return None
        return PublicStats(
            followers=stats["followers"],
            posts_count=stats["posts_count"],
            avg_views=stats["avg_views"],
            resolved_handle=stats.get("channel_title"),
        )
