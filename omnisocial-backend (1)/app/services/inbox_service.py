from datetime import datetime, timedelta, timezone
import httpx
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.services import analytics_service


async def _fetch_youtube_comments(channel_handle: str) -> list[dict]:
    settings = get_settings()
    if not settings.YOUTUBE_API_KEY:
        return []

    # Get public channel video comments if possible
    # We query search for videos from channel
    comments = []
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            search_url = "https://www.googleapis.com/youtube/v3/search"
            res = await client.get(
                search_url,
                params={
                    "part": "snippet",
                    "q": channel_handle,
                    "type": "video",
                    "maxResults": 3,
                    "key": settings.YOUTUBE_API_KEY,
                },
            )
            if res.status_code == 200:
                items = res.json().get("items", [])
                for item in items:
                    video_id = item.get("id", {}).get("videoId")
                    video_title = item.get("snippet", {}).get("title", "Video")
                    if not video_id:
                        continue
                    comm_res = await client.get(
                        "https://www.googleapis.com/youtube/v3/commentThreads",
                        params={
                            "part": "snippet",
                            "videoId": video_id,
                            "maxResults": 5,
                            "key": settings.YOUTUBE_API_KEY,
                        },
                    )
                    if comm_res.status_code == 200:
                        c_items = comm_res.json().get("items", [])
                        for c in c_items:
                            top = c.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
                            comments.append({
                                "id": f"yt-{c.get('id')}",
                                "platform": "youtube",
                                "author": top.get("authorDisplayName", "YouTube User"),
                                "avatar": top.get("authorProfileImageUrl", ""),
                                "content": top.get("textDisplay", ""),
                                "post_title": video_title,
                                "created_at": top.get("publishedAt", datetime.now(timezone.utc).isoformat()),
                                "unread": True,
                                "type": "comment",
                            })
    except Exception as e:
        print(f"[Inbox YouTube] Exception: {e}")
    return comments


async def _fetch_github_comments(username: str) -> list[dict]:
    # Fetch public events for the GitHub user
    comments = []
    cleaned = username.strip().lstrip("@")
    if not cleaned:
        return []
    try:
        async with httpx.AsyncClient(timeout=10, headers={"Accept": "application/vnd.github+json"}) as client:
            res = await client.get(f"https://api.github.com/users/{cleaned}/events/public")
            if res.status_code == 200:
                events = res.json()[:10]
                for ev in events:
                    if ev.get("type") in ["IssueCommentEvent", "PushEvent", "PullRequestReviewCommentEvent"]:
                        payload = ev.get("payload", {})
                        comment_obj = payload.get("comment", {})
                        repo_name = ev.get("repo", {}).get("name", "Repository")
                        actor = ev.get("actor", {})
                        comments.append({
                            "id": f"gh-{ev.get('id')}",
                            "platform": "github",
                            "author": actor.get("display_login") or actor.get("login", "GitHub User"),
                            "avatar": actor.get("avatar_url", ""),
                            "content": comment_obj.get("body") or f"Pushed to {repo_name}",
                            "post_title": repo_name,
                            "created_at": ev.get("created_at", datetime.now(timezone.utc).isoformat()),
                            "unread": True,
                            "type": "mention",
                        })
    except Exception as e:
        print(f"[Inbox GitHub] Exception: {e}")
    return comments


def _get_demo_inbox_items(user_id: str, connected_platforms: list[str]) -> list[dict]:
    now = datetime.now(timezone.utc)
    demo_items = [
        {
            "id": "inbox-1",
            "platform": "youtube",
            "author": "Alex Rivera",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80",
            "content": "Loved this breakdown! Could you cover how you optimized the renderer in the next video?",
            "post_title": "10 AI Tools Every Creator Needs in 2026",
            "created_at": (now - timedelta(minutes=25)).isoformat(),
            "unread": True,
            "type": "comment",
        },
        {
            "id": "inbox-2",
            "platform": "github",
            "author": "dev_sam",
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80",
            "content": "Submitted a PR fixing the theme toggle state synchronization. Please review when free!",
            "post_title": "omnisocial-core / PR #42",
            "created_at": (now - timedelta(hours=2)).isoformat(),
            "unread": True,
            "type": "pull_request",
        },
        {
            "id": "inbox-3",
            "platform": "reddit",
            "author": "u/TechExplorer99",
            "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=100&auto=format&fit=crop&q=80",
            "content": "Great discussion thread. Upvoted and shared on r/webdev!",
            "post_title": "How we scaled our social dashboard to 100k views",
            "created_at": (now - timedelta(hours=5)).isoformat(),
            "unread": False,
            "type": "comment",
        },
        {
            "id": "inbox-4",
            "platform": "devto",
            "author": "Sarah Chen",
            "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop&q=80",
            "content": "Super clear tutorial. Added this to my reading list!",
            "post_title": "Building Modern Dashboards with FastAPI & React",
            "created_at": (now - timedelta(days=1)).isoformat(),
            "unread": False,
            "type": "comment",
        },
        {
            "id": "inbox-5",
            "platform": "youtube",
            "author": "Marcus Brody",
            "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80",
            "content": "This saved me hours of debugging. Subscribed!",
            "post_title": "FastAPI Setup & Best Practices Guide",
            "created_at": (now - timedelta(days=2)).isoformat(),
            "unread": False,
            "type": "comment",
        },
        {
            "id": "inbox-6",
            "platform": "instagram",
            "author": "elena_designs",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80",
            "content": "Love the aesthetic on this reel! What camera setup do you use?",
            "post_title": "Reel: Behind the Scenes of AI Dashboard Design",
            "created_at": (now - timedelta(minutes=40)).isoformat(),
            "unread": True,
            "type": "comment",
        },
    ]
    return demo_items


async def get_inbox_messages(db: Session, user_id: str, platform: str | None = None, unread_only: bool = False) -> list[dict]:
    summaries = analytics_service.get_platform_summaries(db, user_id)
    connected_platforms = [s["platform"] for s in summaries if s["connected"]]
    
    messages = []
    
    # Live fetches for connected YouTube or GitHub
    for s in summaries:
        if not s["connected"]:
            continue
        if s["platform"] == "youtube" and s["handle"]:
            yt_messages = await _fetch_youtube_comments(s["handle"])
            messages.extend(yt_messages)
        elif s["platform"] == "github" and s["handle"]:
            gh_messages = await _fetch_github_comments(s["handle"])
            messages.extend(gh_messages)

    # Always include demo item baseline so inbox is richly populated
    messages.extend(_get_demo_inbox_items(user_id, connected_platforms))

    # Deduplicate by ID
    unique_messages = []
    seen = set()
    for m in messages:
        if m["id"] not in seen:
            seen.add(m["id"])
            unique_messages.append(m)

    # Filter by platform
    if platform and platform != "all":
        unique_messages = [m for m in unique_messages if m["platform"] == platform]

    # Filter by unread
    if unread_only:
        unique_messages = [m for m in unique_messages if m["unread"]]

    # Sort by created_at descending
    unique_messages.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return unique_messages
