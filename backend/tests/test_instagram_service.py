"""
Tests for the Instagram scraping service.

Uses respx to mock httpx calls to Instagram's endpoint - these tests
never hit the real network, so they're fast and don't depend on
Instagram's live behavior (which can change or block requests at any
time).
"""
import respx
from httpx import Response

from app.services import instagram_service


@respx.mock
async def test_returns_live_stats_on_success():
    respx.get(
        "https://www.instagram.com/api/v1/users/web_profile_info/",
        params={"username": "testuser"},
    ).mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "user": {
                        "username": "testuser",
                        "edge_followed_by": {"count": 1000},
                        "edge_owner_to_timeline_media": {"count": 50},
                    }
                }
            },
        )
    )

    stats = await instagram_service.fetch_user_stats("testuser")

    assert stats is not None
    assert stats["followers"] == 1000
    assert stats["posts_count"] == 50
    assert stats["avg_views"] == 120  # 1000 * 0.12


@respx.mock
async def test_returns_none_on_non_200_response():
    respx.get(
        "https://www.instagram.com/api/v1/users/web_profile_info/",
        params={"username": "blockeduser"},
    ).mock(return_value=Response(429))

    stats = await instagram_service.fetch_user_stats("blockeduser")

    # Must NOT fabricate numbers - a blocked/failed request means no data,
    # not made-up data.
    assert stats is None


@respx.mock
async def test_returns_none_on_network_error():
    import httpx

    respx.get(
        "https://www.instagram.com/api/v1/users/web_profile_info/",
        params={"username": "networkfail"},
    ).mock(side_effect=httpx.ConnectError("connection reset"))

    stats = await instagram_service.fetch_user_stats("networkfail")

    assert stats is None


async def test_empty_handle_returns_none():
    assert await instagram_service.fetch_user_stats("") is None
    assert await instagram_service.fetch_user_stats("   ") is None


@respx.mock
async def test_strips_at_symbol_and_whitespace():
    route = respx.get(
        "https://www.instagram.com/api/v1/users/web_profile_info/",
        params={"username": "cleanhandle"},
    ).mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "user": {
                        "username": "cleanhandle",
                        "edge_followed_by": {"count": 5},
                        "edge_owner_to_timeline_media": {"count": 1},
                    }
                }
            },
        )
    )

    stats = await instagram_service.fetch_user_stats("  @CleanHandle  ")

    assert route.called
    assert stats["username"] == "cleanhandle"


@respx.mock
async def test_second_call_uses_cache_not_network():
    instagram_service._CACHE.clear()
    route = respx.get(
        "https://www.instagram.com/api/v1/users/web_profile_info/",
        params={"username": "cacheduser"},
    ).mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "user": {
                        "username": "cacheduser",
                        "edge_followed_by": {"count": 42},
                        "edge_owner_to_timeline_media": {"count": 3},
                    }
                }
            },
        )
    )

    first = await instagram_service.fetch_user_stats("cacheduser")
    second = await instagram_service.fetch_user_stats("cacheduser")

    assert first == second
    assert route.call_count == 1  # second call served from cache, no network hit
