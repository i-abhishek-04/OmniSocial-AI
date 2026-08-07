"""Tests that the app refuses to boot in production with the default
(insecure) JWT secret, but boots fine with a real one or in dev."""
import pytest

from app.core.config import Settings


def test_production_with_default_secret_raises():
    with pytest.raises(ValueError, match="JWT_SECRET must be set"):
        Settings(ENV="production", JWT_SECRET="dev-only-insecure-secret-change-me")


def test_production_with_custom_secret_is_fine():
    s = Settings(ENV="production", JWT_SECRET="a-real-random-secret")
    assert s.JWT_SECRET == "a-real-random-secret"


def test_development_with_default_secret_is_fine():
    s = Settings(ENV="development", JWT_SECRET="dev-only-insecure-secret-change-me")
    assert s.ENV == "development"
