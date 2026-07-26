import httpx

from app.core.config import get_settings


def _fallback_completion(user_message: str) -> str:
    """Return a simple fallback completion when external AI APIs are unavailable."""
    return f"Unable to generate completion right now. You said: {user_message}"


async def generate_completion(system_prompt: str, user_message: str) -> str:
    settings = get_settings()

    # 1. Try Groq API if GROQ_API_KEY is provided
    groq_key = getattr(settings, "GROQ_API_KEY", "") or (settings.GEMINI_API_KEY if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.startswith("gsk_") else "")
    if groq_key:
        print(f"[AI Service] Calling Groq API (key=...{groq_key[-6:]})")
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                res = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message},
                        ],
                        "temperature": 0.7,
                    },
                )
                if res.status_code == 200:
                    text = res.json()["choices"][0]["message"]["content"]
                    print(f"[Groq AI] Got response ({len(text)} chars)")
                    return text
                else:
                    print(f"[Groq AI] API error {res.status_code}")
        except Exception as e:
            print(f"[Groq AI] Exception: {e}")

    # 2. Try Gemini API if GEMINI_API_KEY is set and valid
    if settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("gsk_"):
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{settings.GEMINI_MODEL}:generateContent"
            f"?key={settings.GEMINI_API_KEY}"
        )
        print(f"[Gemini] Calling model={settings.GEMINI_MODEL}, key=...{settings.GEMINI_API_KEY[-6:]}")

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    url,
                    json={
                        "contents": [
                            {
                                "parts": [
                                    {
                                        "text": f"{system_prompt}\n\nUser: {user_message}"
                                    }
                                ]
                            }
                        ]
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"[Gemini] Got response ({len(text)} chars)")
                    return text
                else:
                    print(f"[Gemini] API error {response.status_code}")

        except Exception as e:
            print(f"[Gemini] Exception: {e}")

    return _fallback_completion(user_message)