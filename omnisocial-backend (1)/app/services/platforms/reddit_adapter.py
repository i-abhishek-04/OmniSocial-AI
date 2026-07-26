from app.services import reddit_service
from app.services.platforms.base import PlatformAdapter, PublicStats
from app.services.platforms.placeholder_adapter import DEFAULT_COMING_SOON_MESSAGE


class RedditAdapter(PlatformAdapter):
    platform_id = "reddit"
    display_name = "Reddit"
    color = "#FF4500"
    is_live = False
    coming_soon_message = DEFAULT_COMING_SOON_MESSAGE

    async def fetch_public_stats(self, handle: str) -> PublicStats | None:
        stats = await reddit_service.fetch_user_stats(handle)
        if not stats:
            return None
        return PublicStats(
            followers=stats["followers"],
            posts_count=stats["posts_count"],
            avg_views=stats["avg_views"],
            resolved_handle=stats.get("username"),
        )
