"""Database session and metadata helpers."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./taskforge.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db() -> None:
    # Lazy import to avoid circular dependency during module import.
    from . import models  # noqa: WPS433

    models.Base.metadata.create_all(bind=engine)
