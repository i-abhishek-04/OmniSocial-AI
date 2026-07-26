"""
Platform adapter contract.

This is the one interface every platform integration implements. Adding a
new platform later means: write one adapter class + register it in
registry.py. Nothing in routers/services/schemas has to change.

Two kinds of adapters:

  - Live adapters (is_live=True): wrap a real public API call. See
    youtube_adapter.py / github_adapter.py / reddit_adapter.py /
    devto_adapter.py.
  - Placeholder adapters (is_live=False): platforms that need OAuth/business
    verification we don't have yet (Instagram, LinkedIn, TikTok, Facebook,
    X). fetch_public_stats is never called for these - the dashboard
    renders them as disabled "Coming Soon" cards instead.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PublicStats:
    """Normalized shape every live adapter maps its API response into,
    so analytics_service never needs to know which platform it's talking
    to."""

    followers: int
    posts_count: int
    avg_views: int
    resolved_handle: str | None = None  # e.g. the channel/repo/user title


class PlatformAdapter(ABC):
    """One entry per platform. See module docstring."""

    platform_id: str
    display_name: str
    color: str
    is_live: bool = False

    # Only set (and only shown) on placeholder adapters.
    coming_soon_message: str | None = None

    async def fetch_public_stats(self, handle: str) -> PublicStats | None:
        """Fetch real public stats for `handle`.

        Only ever called when is_live is True. Must never raise - any
        failure (bad handle, network error, rate limit) returns None so
        callers fall back to demo data instead of hard-failing a connect
        request.
        """
        return None
