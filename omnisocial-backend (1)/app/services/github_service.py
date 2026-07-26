"""
GitHub REST API integration.

The single layer permitted to call GitHub's API. Uses only unauthenticated
public endpoints (a username is all that's needed) - GITHUB_TOKEN in
config is optional and only raises the rate limit (60/hr unauthenticated
vs 5,000/hr authenticated), it is never required for the lookup to work.

Mapping onto our normalized stats shape (see platforms/base.py):
  - followers    -> GitHub follower count (real, direct match)
  - posts_count  -> public repo count
  - avg_views    -> average stars per public repo (GitHub doesn't expose
                     view counts publicly, so total stars / repos is the
                     closest public proxy for "how much traction does
                     this account's output get")

Returns None on any failure (bad username, network error, rate limit) so
callers fall back to demo data - a connect request should never hard-fail
just because live data wasn't available.
"""
import httpx

from app.core.config import get_settings

GITHUB_API_URL = "https://api.github.com"


def _headers() -> dict:
    settings = get_settings()
    headers = {"Accept": "application/vnd.github+json"}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"
    return headers


async def fetch_user_stats(username: str) -> dict | None:
    """Look up a GitHub username and return public follower/repo/star
    stats, or None if unavailable."""
    cleaned = username.strip().lstrip("@")
    if not cleaned:
        return None

    try:
        async with httpx.AsyncClient(timeout=10, headers=_headers()) as client:
            user_resp = await client.get(f"{GITHUB_API_URL}/users/{cleaned}")
            if user_resp.status_code == 404:
                print(f"[GitHub] User '{cleaned}' not found (404)")
                return None
            user_resp.raise_for_status()
            user = user_resp.json()

            total_stars = 0
            repos_resp = await client.get(
                f"{GITHUB_API_URL}/users/{cleaned}/repos",
                params={"per_page": 100, "sort": "updated"},
            )
            if repos_resp.status_code == 200:
                for repo in repos_resp.json():
                    total_stars += repo.get("stargazers_count", 0)
    except Exception as e:
        print(f"[GitHub] Error fetching stats for '{cleaned}': {e}")
        return None

    public_repos = int(user.get("public_repos", 0))
    avg_stars = int(total_stars / public_repos) if public_repos else 0

    print(f"[GitHub] Found user '{cleaned}': {user.get('followers', 0)} followers, {public_repos} repos, {total_stars} stars")

    return {
        "login": user.get("login", cleaned),
        "followers": int(user.get("followers", 0)),
        "posts_count": public_repos,
        "avg_views": avg_stars,
        "total_stars": total_stars,
    }

