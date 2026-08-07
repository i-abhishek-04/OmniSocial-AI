"""
Shared pytest fixtures.

Each test gets a fresh in-memory SQLite DB and a TestClient wired to use
it (via FastAPI's dependency override), so tests never touch the real
omnisocial.db file and never leak state between each other.
"""
import os

os.environ.setdefault("ENV", "test")
os.environ.setdefault("JWT_SECRET", "test-secret-not-for-production")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture()
def db_session():
    # StaticPool keeps a single shared connection alive for the whole
    # in-memory DB's lifetime — without it, every new connection to
    # ":memory:" gets its own blank database and "no such table" errors.
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    from app.models import user, chat, social_account, scheduled_post  # noqa: F401

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Reset the in-memory rate limiter's counters between tests so limits
    # from one test don't bleed into another.
    from app.core.rate_limit import limiter

    limiter.reset()

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture()
def registered_user(client):
    payload = {
        "email": "jane@example.com",
        "password": "supersecret123",
        "full_name": "Jane Doe",
        "niche": "Tech",
    }
    res = client.post("/auth/register", json=payload)
    body = res.json()
    return {
        "payload": payload,
        "token": body["data"]["access_token"],
        "user": body["data"]["user"],
    }


@pytest.fixture()
def auth_headers(registered_user):
    return {"Authorization": f"Bearer {registered_user['token']}"}
