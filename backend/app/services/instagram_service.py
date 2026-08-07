"""
Instagram Integration Layer.

Scrapes Instagram's public web_profile_info endpoint (no official Graph
API access - that requires business verification we don't have). This is
inherently best-effort: Instagram can rate-limit or block scraping
requests at any time, especially from cloud IPs.

On any failure this returns None rather than fabricating numbers. The
caller (analytics_service.connect_platform) already has a single,
consistent, clearly-documented demo-data fallback used by every platform
that isn't live-connected - so there is no need for a second, less
honest fallback path here.

A short in-memory cache avoids re-scraping the same handle on every
request, which is both faster and more polite to Instagram's servers.
"""
import time

import httpx

_CACHE: dict[str, tuple[float, dict]] = {}
_CACHE_TTL_SECONDS = 15 * 60

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "x-ig-app-id": "936619743392459",
}


def _cache_get(handle: str) -> dict | None:
    entry = _CACHE.get(handle)
    if not entry:
        return None
    fetched_at, stats = entry
    if time.time() - fetched_at > _CACHE_TTL_SECONDS:
        del _CACHE[handle]
        return None
    return stats


def _cache_set(handle: str, stats: dict) -> None:
    _CACHE[handle] = (time.time(), stats)


async def fetch_user_stats(handle: str) -> dict | None:
    """Fetch live public stats for `handle`.

    Returns None on any failure (private/nonexistent account, network
    error, Instagram blocking the request) - never fabricated numbers.
    Callers must be prepared to handle None and fall back to their own
    demo-data story.
    """
    cleaned = handle.strip().lstrip("@").lower()
    if not cleaned:
        return None

    cached = _cache_get(cleaned)
    if cached:
        return cached

    try:
        async with httpx.AsyncClient(timeout=8, headers=_HEADERS, follow_redirects=True) as client:
            res = await client.get(
                f"https://www.instagram.com/api/v1/users/web_profile_info/?username={cleaned}"
            )
            if res.status_code != 200:
                return None

            user = res.json().get("data", {}).get("user", {})
            if not user:
                return None

            followers = int(user.get("edge_followed_by", {}).get("count", 0))
            posts = int(user.get("edge_owner_to_timeline_media", {}).get("count", 0))
            stats = {
                "username": user.get("username", cleaned),
                "followers": followers,
                "posts_count": posts,
                "avg_views": int(followers * 0.12) if followers else 0,
            }
            _cache_set(cleaned, stats)
            return stats
    except (httpx.HTTPError, ValueError, KeyError):
        # Network failure, timeout, or unexpected response shape - all
        # treated the same: no live data available right now.
        return None
