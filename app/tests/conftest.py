"""Test fixtures and setup configuration for database and API tests."""

import os
from typing import Generator

import psycopg2
import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db import Base, SessionLocal, engine
from app.dependencies import get_db
from app.main import app

# Load .env file
load_dotenv(find_dotenv())

# Always use test DB for this file
POSTGRES_DB = os.getenv('POSTGRES_TEST_DB')


# ✅ Ensure the test DB exists before anything else
@pytest.fixture(scope='session', autouse=True)
def ensure_test_db_exists() -> None:
    """Ensures the test database exists and is
    properly initialized before any tests run."""
    conn = psycopg2.connect(
        dbname='postgres',
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432'),
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_DB}'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f'CREATE DATABASE {POSTGRES_DB}')
        print(f'✅ Created test database: {POSTGRES_DB}')
    else:
        print(f"ℹ️ Test database '{POSTGRES_DB}' already exists")

    cursor.close()
    conn.close()

    # ✅ Now create the schema after DB is guaranteed to exist
    Base.metadata.create_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_db(_ensure_test_db_exists: None) -> None:
    """Truncate all tables after ensure_test_db_exists has run."""
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())


# Provide a clean DB session per test
# pylint: disable=redefined-outer-name
@pytest.fixture(scope='function')
def db() -> Session:
    """Provides a SQLAlchemy session for test cases.

    Yields:
        Session: A SQLAlchemy session with rollback after test execution.
    """
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


# ✅ Provide a FastAPI test client with DB override
@pytest.fixture(scope='function')
def client(db: Session) -> TestClient:
    """Provides a FastAPI TestClient with the database dependency overridden.

    Args:
        db (Session): The SQLAlchemy session provided by the `db` fixture.

    Yields:
        TestClient: A FastAPI test client instance with DB override.
    """

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db  # type: ignore[attr-defined]

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()  # type: ignore[attr-defined]
