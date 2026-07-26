"""
Shared constants.

Display names, "is this platform live" status, and coming-soon messaging
are all derived from services/platforms/registry.py - the single source
of truth - so this file never needs manual edits when a platform is
added or promoted from placeholder to live.
"""
from app.models.social_account import SUPPORTED_PLATFORMS
from app.services.platforms.registry import COMING_SOON_PLATFORM_IDS, LIVE_PLATFORM_IDS, PLATFORM_REGISTRY

PLATFORM_DISPLAY_NAMES = {p: a.display_name for p, a in PLATFORM_REGISTRY.items()}

__all__ = [
    "SUPPORTED_PLATFORMS",
    "PLATFORM_DISPLAY_NAMES",
    "LIVE_PLATFORM_IDS",
    "COMING_SOON_PLATFORM_IDS",
]
