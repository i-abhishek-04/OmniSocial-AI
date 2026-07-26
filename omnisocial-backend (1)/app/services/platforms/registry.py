"""
Platform registry - the single source of truth for which platforms exist,
in what order, and which adapter handles each one.
"""
from app.services.platforms.base import PlatformAdapter
from app.services.platforms.devto_adapter import DevToAdapter
from app.services.platforms.github_adapter import GitHubAdapter
from app.services.platforms.instagram_adapter import InstagramAdapter
from app.services.platforms.placeholder_adapter import (
    FacebookAdapter,
    LinkedInAdapter,
    TikTokAdapter,
    TwitterAdapter,
)
from app.services.platforms.reddit_adapter import RedditAdapter
from app.services.platforms.youtube_adapter import YouTubeAdapter

PLATFORM_REGISTRY: dict[str, PlatformAdapter] = {
    # Fully functional - real public APIs.
    "youtube": YouTubeAdapter(),
    "github": GitHubAdapter(),
    "instagram": InstagramAdapter(),
    # Coming soon - disabled placeholder cards.
    "reddit": RedditAdapter(),
    "devto": DevToAdapter(),
    "linkedin": LinkedInAdapter(),
    "tiktok": TikTokAdapter(),
    "facebook": FacebookAdapter(),
    "x": TwitterAdapter(),
}

ALL_PLATFORM_IDS: list[str] = list(PLATFORM_REGISTRY.keys())
LIVE_PLATFORM_IDS: list[str] = [p for p, a in PLATFORM_REGISTRY.items() if a.is_live]
COMING_SOON_PLATFORM_IDS: list[str] = [p for p, a in PLATFORM_REGISTRY.items() if not a.is_live]


def get_platform_registry() -> dict[str, PlatformAdapter]:
    return {
        "youtube": YouTubeAdapter(),
        "github": GitHubAdapter(),
        "instagram": InstagramAdapter(),
        "reddit": RedditAdapter(),
        "devto": DevToAdapter(),
        "linkedin": LinkedInAdapter(),
        "tiktok": TikTokAdapter(),
        "facebook": FacebookAdapter(),
        "x": TwitterAdapter(),
    }


def get_adapter(platform_id: str) -> PlatformAdapter | None:
    return get_platform_registry().get(platform_id)
