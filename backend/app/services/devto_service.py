"""
Dev.to (Forem) public API integration.

The single layer permitted to call Dev.to's API. No auth needed for
public reads - just a username.

IMPORTANT LIMITATION (documented, not hidden): Dev.to's public API does
not expose a follower count or page-view counts for a user (those are
only available to the authenticated owner via a personal API key on
/api/articles/me). So this maps onto our normalized shape as an honest
proxy rather than a 1:1 match:
  - followers    -> total public reactions across the user's articles
                     (the closest public signal for "how big is this
                     creator's audience")
  - posts_count  -> number of published public articles
  - avg_views    -> average comments per article (public engagement
                     proxy; not literal view count)

Returns None on any failure (unknown username, network error, rate
limit) so callers fall back to demo data.
"""
import httpx

DEVTO_API_URL = "https://dev.to/api"


async def fetch_user_stats(username: str) -> dict | None:
    """Look up a Dev.to username and return public article-engagement
    stats, or None if unavailable."""
    cleaned = username.strip().lstrip("@")
    if not cleaned:
        return None

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            profile_resp = await client.get(
                f"{DEVTO_API_URL}/users/by_username", params={"url": cleaned}
            )
            if profile_resp.status_code == 404:
                return None
            profile_resp.raise_for_status()
            profile = profile_resp.json()

            articles_resp = await client.get(
                f"{DEVTO_API_URL}/articles", params={"username": cleaned, "per_page": 100}
            )
            articles_resp.raise_for_status()
            articles = articles_resp.json()
    except Exception:
        return None

    posts_count = len(articles)
    total_reactions = sum(a.get("public_reactions_count", 0) for a in articles)
    total_comments = sum(a.get("comments_count", 0) for a in articles)
    avg_comments = int(total_comments / posts_count) if posts_count else 0

    return {
        "username": profile.get("username", cleaned),
        "followers": total_reactions,
        "posts_count": posts_count,
        "avg_views": avg_comments,
    }
