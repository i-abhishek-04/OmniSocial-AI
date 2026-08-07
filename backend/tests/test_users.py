"""Tests for /users/* endpoints."""


def test_get_me_requires_auth(client):
    res = client.get("/users/me")
    assert res.status_code == 401


def test_get_me_returns_profile(client, auth_headers):
    res = client.get("/users/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["data"]["full_name"] == "Jane Doe"


def test_update_me_changes_full_name(client, auth_headers):
    res = client.put("/users/me", json={"full_name": "Jane Updated"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["data"]["full_name"] == "Jane Updated"

    # verify the change persisted
    check = client.get("/users/me", headers=auth_headers)
    assert check.json()["data"]["full_name"] == "Jane Updated"


def test_update_me_without_auth_is_rejected(client):
    res = client.put("/users/me", json={"full_name": "Nope"})
    assert res.status_code == 401
