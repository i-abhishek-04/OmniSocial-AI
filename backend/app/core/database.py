"""
Database engine and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import get_settings

settings = get_settings()
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if db_url.startswith("postgresql://") and "sslmode=" not in db_url:
    delimiter = "&" if "?" in db_url else "?"
    db_url = f"{db_url}{delimiter}sslmode=require"

connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(db_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Import models so they're registered on Base.metadata before create_all
    from app.models import user, chat, social_account, scheduled_post  # noqa: F401
    Base.metadata.create_all(bind=engine)

