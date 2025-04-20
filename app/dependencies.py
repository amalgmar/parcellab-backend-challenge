"""Shared dependency functions for FastAPI routes."""

from typing import Generator

from _pytest.main import Session

from app.db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provides a database session to route handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
