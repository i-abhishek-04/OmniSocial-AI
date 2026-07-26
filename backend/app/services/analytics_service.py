"""
Analytics business logic - the demo data engine.

DEMO DATA NOTE (read this before wiring up more real platforms):
This service generates realistic-looking analytics deterministically
(seeded by user_id + platform, so numbers stay stable across requests/
refreshes instead of jumping around randomly) as a fallback for platforms
that either aren't connected yet or aren't live-capable at all.

Real platform data flows through services/platforms/registry.py: every
live adapter (YouTube, GitHub, Reddit, Dev.to) can be asked for real
public stats via connect_platform() below; coming-soon platforms
(Instagram, LinkedIn, TikTok, Facebook, X) are never fetched and never
marked connected - see PLATFORM_REGISTRY for the single source of truth
on which platforms are which.
"""
import hashlib
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.social_account import SUPPORTED_PLATFORMS
from app.repository import social_repository
from app.services.platforms.registry import COMING_SOON_PLATFORM_IDS, LIVE_PLATFORM_IDS, PLATFORM_REGISTRY, get_adapter
from app.utils.constants import PLATFORM_DISPLAY_NAMES

# Colors now come from each platform's adapter (one source of truth) rather
# than a second hardcoded dict that could drift out of sync with it.
PLATFORM_COLORS = {platform: adapter.color for platform, adapter in PLATFORM_REGISTRY.items()}

# Base scale per platform so e.g. YouTube subs and GitHub followers land in
# plausible, distinct ranges rather than all looking the same. Only used
# for demo fallback numbers (no live API key set, or platform is coming
# soon) - real connections use live adapter data instead.
PLATFORM_BASE_RANGE = {
    "youtube": (8_000, 420_000),
    "github": (50, 25_000),
    "reddit": (500, 150_000),
    "devto": (200, 40_000),
    "instagram": (5_000, 380_000),
    "tiktok": (10_000, 900_000),
    "facebook": (2_000, 150_000),
    "x": (1_500, 120_000),
    "linkedin": (800, 60_000),
}


def _seed(user_id: str, platform: str, salt: str = "") -> random.Random:
    key = f"{user_id}:{platform}:{salt}".encode()
    digest = hashlib.sha256(key).hexdigest()
    return random.Random(int(digest[:16], 16))


def generate_snapshot_stats(user_id: str, platform: str) -> dict:
    rng = _seed(user_id, platform)
    lo, hi = PLATFORM_BASE_RANGE.get(platform, (1_000, 100_000))
    followers = rng.randint(lo, hi)
    engagement_rate = round(rng.uniform(1.2, 9.5), 2)
    avg_views = int(followers * rng.uniform(0.15, 0.9))
    posts_count = rng.randint(30, 900)
    growth_30d = round(rng.uniform(-2.5, 18.0), 2)
    if platform in COMING_SOON_PLATFORM_IDS:
        # Coming-soon platforms are never connectable yet, so they must
        # never randomly seed as "connected" - the dashboard renders them
        # as disabled placeholder cards regardless of these numbers.
        connected = False
    else:
        # ~70% of live platforms start out "connected" in the demo so the
        # dashboard looks populated; the rest show as connectable.
        connected = rng.random() < 0.7
    return {
        "connected": connected,
        "followers": followers,
        "engagement_rate": engagement_rate,
        "avg_views": avg_views,
        "posts_count": posts_count,
        "growth_30d": growth_30d,
    }


def generate_timeseries(user_id: str, platform: str, current_followers: int, days: int = 30) -> list[dict]:
    rng = _seed(user_id, platform, salt="timeseries")
    daily_growth = rng.uniform(0.001, 0.01)
    points = []
    followers = current_followers / ((1 + daily_growth) ** days)
    today = datetime.now(timezone.utc).date()
    for i in range(days, -1, -1):
        date = today - timedelta(days=i)
        noise = rng.uniform(-0.01, 0.015)
        followers = max(0, followers * (1 + daily_growth + noise))
        views = int(followers * rng.uniform(0.05, 0.3))
        engagement = round(rng.uniform(1.0, 10.0), 2)
        points.append({
            "date": date.isoformat(),
            "followers": int(followers),
            "views": views,
            "engagement_rate": engagement,
        })
    return points


def generate_monthly_revenue(user_id: str, platform: str, followers: int, months: int = 6) -> list[float]:
    rng = _seed(user_id, platform, salt="revenue")
    # Rough demo CPM-style multiplier so bigger accounts show bigger revenue.
    base = (followers / 1000) * rng.uniform(2.0, 14.0)
    values = []
    amount = base * rng.uniform(0.6, 1.0)
    for _ in range(months):
        amount = max(0, amount * rng.uniform(0.85, 1.25))
        values.append(round(amount, 2))
    return values


def get_platform_summaries(db: Session, user_id: str) -> list[dict]:
    accounts = social_repository.ensure_seeded(db, user_id, user_email=user_id)
    summaries = []
    for account in accounts:
        adapter = get_adapter(account.platform)
        monthly_revenue = generate_monthly_revenue(
            user_id, account.platform, account.followers, months=1
        )[0] if account.connected else 0.0
        summaries.append({
            "platform": account.platform,
            "display_name": PLATFORM_DISPLAY_NAMES[account.platform],
            "connected": account.connected,
            "handle": account.handle,
            "followers": account.followers if account.connected else 0,
            "engagement_rate": account.engagement_rate if account.connected else 0.0,
            "avg_views": account.avg_views if account.connected else 0,
            "posts_count": account.posts_count if account.connected else 0,
            "growth_30d": account.growth_30d if account.connected else 0.0,
            "monthly_revenue": monthly_revenue,
            "color": PLATFORM_COLORS[account.platform],
            "is_live": account.is_live,
            "is_supported": adapter.is_live if adapter else False,
            "coming_soon_message": None if (adapter and adapter.is_live) else (adapter.coming_soon_message if adapter else None),
        })
    return summaries


def get_overview(db: Session, user_id: str, user_email: str) -> dict:
    social_repository.ensure_seeded(db, user_id, user_email=user_email)
    summaries = get_platform_summaries(db, user_id)
    connected = [s for s in summaries if s["connected"]]

    total_followers = sum(s["followers"] for s in connected)
    total_revenue = sum(s["monthly_revenue"] for s in connected)
    avg_engagement = (
        round(sum(s["engagement_rate"] for s in connected) / len(connected), 2)
        if connected else 0.0
    )
    avg_growth = (
        round(sum(s["growth_30d"] for s in connected) / len(connected), 2)
        if connected else 0.0
    )
    top_platform = max(connected, key=lambda s: s["followers"])["display_name"] if connected else None

    # Combined follower trend across all connected platforms, last 30 days.
    trend_by_date: dict[str, int] = {}
    for s in connected:
        series = generate_timeseries(user_id, s["platform"], s["followers"], days=30)
        for point in series:
            trend_by_date[point["date"]] = trend_by_date.get(point["date"], 0) + point["followers"]
    follower_trend = [{"date": d, "followers": f} for d, f in sorted(trend_by_date.items())]

    return {
        "total_followers": total_followers,
        "total_engagement_rate": avg_engagement,
        "total_monthly_revenue": round(total_revenue, 2),
        "avg_growth_30d": avg_growth,
        "connected_platforms": len(connected),
        "total_platforms": len(SUPPORTED_PLATFORMS),
        "supported_platforms": len(LIVE_PLATFORM_IDS),
        "coming_soon_platforms": len(COMING_SOON_PLATFORM_IDS),
        "platforms": summaries,
        "follower_trend": follower_trend,
        "top_platform": top_platform,
    }


def get_platform_detail(db: Session, user_id: str, user_email: str, platform: str) -> dict | None:
    if platform not in SUPPORTED_PLATFORMS:
        return None
    social_repository.ensure_seeded(db, user_id, user_email=user_email)
    account = social_repository.get_platform_for_user(db, user_id, platform)
    if not account:
        return None
    adapter = get_adapter(platform)
    timeseries = (
        generate_timeseries(user_id, platform, account.followers, days=30)
        if account.connected else []
    )
    monthly_revenue = generate_monthly_revenue(
        user_id, platform, account.followers, months=1
    )[0] if account.connected else 0.0
    return {
        "platform": platform,
        "display_name": PLATFORM_DISPLAY_NAMES[platform],
        "connected": account.connected,
        "handle": account.handle,
        "followers": account.followers if account.connected else 0,
        "engagement_rate": account.engagement_rate if account.connected else 0.0,
        "avg_views": account.avg_views if account.connected else 0,
        "posts_count": account.posts_count if account.connected else 0,
        "growth_30d": account.growth_30d if account.connected else 0.0,
        "monthly_revenue": monthly_revenue,
        "color": PLATFORM_COLORS[platform],
        "is_live": account.is_live,
        "is_supported": adapter.is_live if adapter else False,
        "coming_soon_message": None if (adapter and adapter.is_live) else (adapter.coming_soon_message if adapter else None),
        "timeseries": timeseries,
    }


def get_revenue(db: Session, user_id: str, user_email: str) -> dict:
    social_repository.ensure_seeded(db, user_id, user_email=user_email)
    summaries = get_platform_summaries(db, user_id)
    connected = [s for s in summaries if s["connected"]]

    months_count = 6
    now = datetime.now(timezone.utc)
    month_labels = []
    m = now
    for i in range(months_count):
        month_labels.append(m.strftime("%b %Y"))
        prev_month = m.month - 1 or 12
        prev_year = m.year - 1 if m.month == 1 else m.year
        m = m.replace(year=prev_year, month=prev_month, day=1)
    month_labels.reverse()

    per_platform_series = {
        s["platform"]: generate_monthly_revenue(user_id, s["platform"], s["followers"], months=months_count)
        for s in connected
    }

    months = []
    for idx, label in enumerate(month_labels):
        by_platform = []
        total = 0.0
        for s in connected:
            amount = per_platform_series[s["platform"]][idx]
            total += amount
            by_platform.append({
                "platform": s["platform"],
                "display_name": s["display_name"],
                "amount": amount,
                "color": s["color"],
            })
        months.append({"month": label, "total": round(total, 2), "by_platform": by_platform})

    total_this_month = months[-1]["total"] if months else 0.0
    total_last_month = months[-2]["total"] if len(months) > 1 else 0.0
    change_pct = (
        round(((total_this_month - total_last_month) / total_last_month) * 100, 2)
        if total_last_month else 0.0
    )

    return {
        "total_this_month": total_this_month,
        "total_last_month": total_last_month,
        "change_pct": change_pct,
        "months": months,
        "breakdown_this_month": months[-1]["by_platform"] if months else [],
    }


async def connect_platform(db: Session, user_id: str, user_email: str, platform: str, handle: str) -> dict | None:
    adapter = get_adapter(platform)
    if adapter is None:
        return None
    if not adapter.is_live:
        # Coming-soon platforms (Instagram, LinkedIn, TikTok, Facebook, X)
        # have no working connect flow yet - the frontend should be
        # showing a disabled button for these, but guard here too.
        return None

    social_repository.ensure_seeded(db, user_id, user_email=user_email)
    account = social_repository.get_platform_for_user(db, user_id, platform)
    if not account:
        return None

    # Every live adapter exposes the same fetch_public_stats(handle)
    # contract, so this works identically for YouTube, GitHub, Reddit, and
    # Dev.to - adding a fifth live platform later needs no change here.
    live_stats = await adapter.fetch_public_stats(handle)

    if live_stats:
        social_repository.update_live_stats(
            db,
            account,
            followers=live_stats.followers,
            posts_count=live_stats.posts_count,
            avg_views=live_stats.avg_views,
        )

    social_repository.set_connected(db, account, connected=True, handle=handle)
    return get_platform_detail(db, user_id, user_email, platform)


def disconnect_platform(db: Session, user_id: str, user_email: str, platform: str) -> dict | None:
    account = social_repository.get_platform_for_user(db, user_id, platform)
    if not account:
        return None
    social_repository.set_connected(db, account, connected=False)
    return get_platform_detail(db, user_id, user_email, platform)
