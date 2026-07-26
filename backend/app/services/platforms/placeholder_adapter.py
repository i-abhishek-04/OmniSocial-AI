"""
Placeholder adapter for platforms whose public APIs require OAuth app
review or business verification we don't have yet. One instance per
platform, all sharing the same behavior: is_live stays False, so
analytics_service never attempts a live fetch, and the frontend renders
these as disabled "Coming Soon" cards instead of connectable ones.
"""
from app.services.platforms.base import PlatformAdapter

DEFAULT_COMING_SOON_MESSAGE = (
    "This platform requires additional API permissions or business "
    "verification. Our modular architecture is already prepared to "
    "support this integration once access becomes available."
)


class PlaceholderAdapter(PlatformAdapter):
    is_live = False

    def __init__(self, platform_id: str, display_name: str, color: str):
        self.platform_id = platform_id
        self.display_name = display_name
        self.color = color
        self.coming_soon_message = DEFAULT_COMING_SOON_MESSAGE


class InstagramAdapter(PlaceholderAdapter):
    def __init__(self):
        super().__init__("instagram", "Instagram", "#E1306C")


class LinkedInAdapter(PlaceholderAdapter):
    def __init__(self):
        super().__init__("linkedin", "LinkedIn", "#0A66C2")


class TikTokAdapter(PlaceholderAdapter):
    def __init__(self):
        super().__init__("tiktok", "TikTok", "#25F4EE")


class FacebookAdapter(PlaceholderAdapter):
    def __init__(self):
        super().__init__("facebook", "Facebook", "#1877F2")


class TwitterAdapter(PlaceholderAdapter):
    def __init__(self):
        super().__init__("x", "X (Twitter)", "#e2e8f0")
