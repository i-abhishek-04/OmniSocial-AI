
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.chat import ChatMessage
from app.repository import chat_repository
from app.services import analytics_service, ai_service


def _build_grounded_reply(user_message: str, overview: dict) -> str | None:
  
    text = user_message.lower()
    platforms = overview["platforms"]
    connected = [p for p in platforms if p["connected"]]

    if any(k in text for k in ["best platform", "top platform", "which platform"]):
        if not connected:
            return "You don't have any platforms connected yet - connect one from the dashboard to see this."
        best = max(connected, key=lambda p: p["followers"])
        return (
            f"{best['display_name']} is your top platform with {best['followers']:,} followers "
            f"and a {best['engagement_rate']}% engagement rate."
        )

    if any(k in text for k in ["revenue", "earning", "money", "income"]):
        return (
            f"You're currently at ${overview['total_monthly_revenue']:,.2f} in estimated monthly revenue "
            f"across {overview['connected_platforms']} connected platforms."
        )

    if any(k in text for k in ["growth", "growing", "trend"]):
        return (
            f"Your average 30-day growth rate is {overview['avg_growth_30d']}% across connected platforms, "
            f"with {overview['total_followers']:,} total followers."
        )

    if any(k in text for k in ["engagement"]):
        return f"Your average engagement rate across connected platforms is {overview['total_engagement_rate']}%."

    if any(k in text for k in ["follower", "audience", "subs", "subscriber"]):
        return f"You have {overview['total_followers']:,} total followers across {overview['connected_platforms']} connected platforms."

    for p in platforms:
        if p["platform"] in text or p["display_name"].lower() in text:
            if not p["connected"]:
                return f"{p['display_name']} isn't connected yet - connect it from the dashboard to see live stats."
            return (
                f"On {p['display_name']}: {p['followers']:,} followers, {p['engagement_rate']}% engagement, "
                f"{p['growth_30d']}% growth over 30 days, ~${p['monthly_revenue']:,.2f}/mo estimated revenue."
            )

    return None


async def send_message(db: Session, user_id: str, user_email: str, message: str) -> ChatMessage:
    try:
        settings = get_settings()

        chat_repository.add_message(db, user_id=user_id, role="user", content=message)

        overview = analytics_service.get_overview(db, user_id, user_email)

        reply_text = None
        has_ai_key = bool(settings.GROQ_API_KEY or settings.GEMINI_API_KEY)

        if has_ai_key:
            summary = (
                f"Total followers: {overview['total_followers']}. "
                f"Monthly revenue: ${overview['total_monthly_revenue']}. "
                f"Avg engagement: {overview['total_engagement_rate']}%. "
                f"Avg 30d growth: {overview['avg_growth_30d']}%. "
                f"Connected platforms: {', '.join(p['display_name'] for p in overview['platforms'] if p['connected']) or 'none'}."
            )
            system_prompt = (
                "You are the AI assistant inside OmniSocial AI, an analytics dashboard for "
                "influencers/creators across 7 platforms. Answer briefly and helpfully using "
                f"this real data about the current user: {summary}"
            )
            completion = await ai_service.generate_completion(system_prompt, message)
            if completion and not completion.startswith("Unable to generate completion"):
                reply_text = completion

        if reply_text is None:
            reply_text = _build_grounded_reply(message, overview)

        if reply_text is None:
            reply_text = "Hello! How can I help you analyze your cross-platform audience and performance today?"

        reply = chat_repository.add_message(db, user_id=user_id, role="assistant", content=reply_text)
        return reply
    except Exception as e:
        print(f"[Chat Service Error]: {e}")
        import traceback
        traceback.print_exc()
        raise e



