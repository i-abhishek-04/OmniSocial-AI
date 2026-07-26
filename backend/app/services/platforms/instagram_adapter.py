from app.services import instagram_service
from app.services.platforms.base import PlatformAdapter, PublicStats


class InstagramAdapter(PlatformAdapter):
    platform_id = "instagram"
    display_name = "Instagram"
    color = "#E1306C"
    is_live = True

    async def fetch_public_stats(self, handle: str) -> PublicStats | None:
        stats = await instagram_service.fetch_user_stats(handle)
        if not stats:
            return None
        return PublicStats(
            followers=stats["followers"],
            posts_count=stats["posts_count"],
            avg_views=stats["avg_views"],
            resolved_handle=stats.get("username"),
        )
