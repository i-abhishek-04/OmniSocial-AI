"""
YouTube Data API v3 integration.

The single layer permitted to call YouTube's public API. Requires only a
free API key (YOUTUBE_API_KEY) - no OAuth, no app review - because we only
ever read a channel's *public* statistics (subscriber/view/video counts),
never anything user-specific.

If YOUTUBE_API_KEY is unset, or the lookup fails for any reason (bad
handle, network error, quota exceeded), `fetch_channel_stats` returns None
and callers are expected to fall back to the existing simulated demo data
- connecting the platform should never hard-fail just because live data
wasn't available.
"""
import httpx

from app.core.config import get_settings

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/channels"


async def fetch_channel_stats(handle: str) -> dict | None:
    """Look up a channel by @handle, legacy username, or channel ID and return its public
    stats, or None if unavailable (missing key, not found, API error)."""
    settings = get_settings()

    if not settings.YOUTUBE_API_KEY or not settings.YOUTUBE_API_KEY.strip():
        print("[YouTube Service Warning] YOUTUBE_API_KEY is unset or empty in .env.")
        return None

    cleaned = handle.strip()
    is_channel_id = cleaned.startswith("UC") and len(cleaned) == 24
    raw_handle = cleaned.lstrip("@")

    async with httpx.AsyncClient(timeout=10) as client:
        payload = None

        if is_channel_id:
            # Query by Channel ID directly
            try:
                resp = await client.get(
                    YOUTUBE_API_URL,
                    params={"part": "snippet,statistics", "id": cleaned, "key": settings.YOUTUBE_API_KEY},
                )
                if resp.status_code == 200:
                    payload = resp.json()
                else:
                    print(f"[YouTube API Error] Status {resp.status_code}: {resp.text}")
            except Exception as e:
                print(f"[YouTube Service Error] Query by ID failed: {e}")
        else:
            # Query by forHandle first (e.g. forHandle=@mkbhd or forHandle=mkbhd)
            for handle_param in [f"@{raw_handle}", raw_handle]:
                try:
                    resp = await client.get(
                        YOUTUBE_API_URL,
                        params={"part": "snippet,statistics", "forHandle": handle_param, "key": settings.YOUTUBE_API_KEY},
                    )
                    if resp.status_code == 200:
                        res_json = resp.json()
                        if res_json.get("items"):
                            payload = res_json
                            break
                    else:
                        print(f"[YouTube API Error] Status {resp.status_code} for handle '{handle_param}': {resp.text}")
                except Exception as e:
                    print(f"[YouTube Service Error] Query by forHandle '{handle_param}' failed: {e}")

            # Fallback to legacy forUsername if forHandle returned no items
            if not payload or not payload.get("items"):
                try:
                    resp = await client.get(
                        YOUTUBE_API_URL,
                        params={"part": "snippet,statistics", "forUsername": raw_handle, "key": settings.YOUTUBE_API_KEY},
                    )
                    if resp.status_code == 200:
                        res_json = resp.json()
                        if res_json.get("items"):
                            payload = res_json
                except Exception as e:
                    print(f"[YouTube Service Error] Query by forUsername '{raw_handle}' failed: {e}")

    if not payload or not payload.get("items"):
        print(f"[YouTube Service Warning] No channel found for handle '{handle}'.")
        return None

    items = payload.get("items", [])
    channel = items[0]
    stats = channel.get("statistics", {})
    snippet = channel.get("snippet", {})

    subscriber_count = int(stats.get("subscriberCount", 0))
    view_count = int(stats.get("viewCount", 0))
    video_count = int(stats.get("videoCount", 0))
    avg_views = int(view_count / video_count) if video_count else 0

    return {
        "channel_title": snippet.get("title", cleaned),
        "followers": subscriber_count,
        "posts_count": video_count,
        "avg_views": avg_views,
        "total_views": view_count,
    }

