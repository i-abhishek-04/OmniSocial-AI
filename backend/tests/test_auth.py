"""Tests for /auth/* endpoints."""


def test_register_creates_user_and_returns_token(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "password": "password123",
            "full_name": "New User",
            "niche": "Fitness",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["data"]["user"]["email"] == "new@example.com"
    assert body["data"]["access_token"]


def test_register_rejects_duplicate_email(client, registered_user):
    res = client.post("/auth/register", json=registered_user["payload"])
    assert res.status_code == 409


def test_register_rejects_short_password(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "short@example.com",
            "password": "abc",
            "full_name": "Short Pw",
        },
    )
    assert res.status_code == 422


def test_login_with_correct_credentials(client, registered_user):
    res = client.post(
        "/auth/login",
        json={
            "email": registered_user["payload"]["email"],
            "password": registered_user["payload"]["password"],
        },
    )
    assert res.status_code == 200
    assert res.json()["data"]["access_token"]


def test_login_with_wrong_password_is_rejected(client, registered_user):
    res = client.post(
        "/auth/login",
        json={"email": registered_user["payload"]["email"], "password": "wrongpassword"},
    )
    assert res.status_code == 401


def test_login_with_unknown_email_is_rejected(client):
    res = client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "whatever123"},
    )
    assert res.status_code == 401


def test_me_requires_authentication(client):
    res = client.get("/auth/me")
    assert res.status_code == 401


def test_me_returns_current_user_with_valid_token(client, auth_headers, registered_user):
    res = client.get("/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["data"]["email"] == registered_user["payload"]["email"]


def test_me_rejects_garbage_token(client):
    res = client.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert res.status_code == 401
