"""
Centralized application settings.

Every other module reads config from here via `get_settings()` - never
from `os.environ` directly.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "OmniSocial AI API"
    ENV: str = "development"

    
    DATABASE_URL: str = "sqlite:///./omnisocial.db"

    # Auth
    JWT_SECRET: str = "dev-only-insecure-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GROQ_API_KEY: str = ""

    
    YOUTUBE_API_KEY: str = ""

    GITHUB_TOKEN: str = ""

    REDDIT_USER_AGENT: str = "OmniSocialAI/1.0 (creator-dashboard)"
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""

    
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,https://omnisocial-ai.vercel.app"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @model_validator(mode="after")
    def _enforce_jwt_secret_in_production(self) -> "Settings":
        """Refuse to boot in production with the default dev JWT secret."""
        if self.ENV.lower() in ("production", "prod") and self.JWT_SECRET == "dev-only-insecure-secret-change-me":
            raise ValueError(
                "JWT_SECRET must be set via environment variable when ENV=production. "
                "Refusing to start with the default insecure development secret."
            )
        return self


def get_settings() -> Settings:
    return Settings()

