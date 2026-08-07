"""Tests that login/register are actually rate-limited (5/minute)."""


def test_login_gets_rate_limited_after_five_attempts(client):
    payload = {"email": "ratelimit@example.com", "password": "wrongpassword"}
    statuses = [client.post("/auth/login", json=payload).status_code for _ in range(6)]

    # First 5 attempts should be normal auth failures (401), the 6th should
    # be blocked by the rate limiter (429) before it even reaches auth logic.
    assert statuses[:5] == [401, 401, 401, 401, 401]
    assert statuses[5] == 429


def test_register_gets_rate_limited_after_five_attempts(client):
    def make_payload(i):
        return {
            "email": f"user{i}@example.com",
            "password": "password123",
            "full_name": f"User {i}",
        }

    statuses = [client.post("/auth/register", json=make_payload(i)).status_code for i in range(6)]

    assert statuses[:5] == [200, 200, 200, 200, 200]
    assert statuses[5] == 429
