from app.services import github_service
from app.services.platforms.base import PlatformAdapter, PublicStats


class GitHubAdapter(PlatformAdapter):
    platform_id = "github"
    display_name = "GitHub"
    color = "#ffffff"
    is_live = True

    async def fetch_public_stats(self, handle: str) -> PublicStats | None:
        stats = await github_service.fetch_user_stats(handle)
        if not stats:
            return None
        return PublicStats(
            followers=stats["followers"],
            posts_count=stats["posts_count"],
            avg_views=stats["avg_views"],
            resolved_handle=stats.get("login"),
        )
