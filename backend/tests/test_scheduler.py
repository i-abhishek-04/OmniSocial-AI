"""Tests for /scheduler/* endpoints (scheduled post CRUD)."""


def _sample_post(**overrides):
    payload = {
        "title": "Launch announcement",
        "content": "We're live!",
        "platforms": ["youtube", "github"],
        "scheduled_at": "2026-09-01T10:00:00Z",
        "status": "scheduled",
    }
    payload.update(overrides)
    return payload


def test_list_posts_empty_initially(client, auth_headers):
    res = client.get("/scheduler/posts", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["data"] == []


def test_create_post(client, auth_headers):
    res = client.post("/scheduler/posts", json=_sample_post(), headers=auth_headers)
    assert res.status_code == 200
    body = res.json()["data"]
    assert body["title"] == "Launch announcement"
    assert body["platforms"] == ["youtube", "github"]


def test_create_post_requires_at_least_one_platform(client, auth_headers):
    res = client.post(
        "/scheduler/posts", json=_sample_post(platforms=[]), headers=auth_headers
    )
    assert res.status_code == 422


def test_update_post(client, auth_headers):
    created = client.post("/scheduler/posts", json=_sample_post(), headers=auth_headers)
    post_id = created.json()["data"]["id"]

    res = client.put(
        f"/scheduler/posts/{post_id}", json={"title": "Updated title"}, headers=auth_headers
    )
    assert res.status_code == 200
    assert res.json()["data"]["title"] == "Updated title"


def test_update_nonexistent_post_returns_404(client, auth_headers):
    res = client.put(
        "/scheduler/posts/does-not-exist", json={"title": "x"}, headers=auth_headers
    )
    assert res.status_code == 404


def test_delete_post(client, auth_headers):
    created = client.post("/scheduler/posts", json=_sample_post(), headers=auth_headers)
    post_id = created.json()["data"]["id"]

    res = client.delete(f"/scheduler/posts/{post_id}", headers=auth_headers)
    assert res.status_code == 200

    listing = client.get("/scheduler/posts", headers=auth_headers)
    assert listing.json()["data"] == []


def test_delete_nonexistent_post_returns_404(client, auth_headers):
    res = client.delete("/scheduler/posts/does-not-exist", headers=auth_headers)
    assert res.status_code == 404


def test_scheduler_endpoints_require_auth(client):
    assert client.get("/scheduler/posts").status_code == 401
    assert client.post("/scheduler/posts", json=_sample_post()).status_code == 401


def test_user_cannot_see_other_users_posts(client, db_session):
    # Create user A and a post for them
    client.post(
        "/auth/register",
        json={"email": "a@example.com", "password": "passwordA1", "full_name": "A"},
    )
    login_a = client.post(
        "/auth/login", json={"email": "a@example.com", "password": "passwordA1"}
    )
    headers_a = {"Authorization": f"Bearer {login_a.json()['data']['access_token']}"}
    client.post("/scheduler/posts", json=_sample_post(), headers=headers_a)

    # Create user B, who should see no posts
    client.post(
        "/auth/register",
        json={"email": "b@example.com", "password": "passwordB1", "full_name": "B"},
    )
    login_b = client.post(
        "/auth/login", json={"email": "b@example.com", "password": "passwordB1"}
    )
    headers_b = {"Authorization": f"Bearer {login_b.json()['data']['access_token']}"}

    res = client.get("/scheduler/posts", headers=headers_b)
    assert res.json()["data"] == []
