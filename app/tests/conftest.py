import os
import sys
import pytest
import psycopg2

from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, SessionLocal, engine
from dotenv import load_dotenv, find_dotenv

# Load .env file
load_dotenv(find_dotenv())

# Always use test DB for this file
POSTGRES_DB = os.getenv("POSTGRES_TEST_DB")


# ✅ Ensure the test DB exists before anything else
@pytest.fixture(scope="session", autouse=True)
def ensure_test_db_exists():
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_DB}'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"CREATE DATABASE {POSTGRES_DB}")
        print(f"✅ Created test database: {POSTGRES_DB}")
    else:
        print(f"ℹ️ Test database '{POSTGRES_DB}' already exists")

    cursor.close()
    conn.close()

    # ✅ Now create the schema after DB is guaranteed to exist
    Base.metadata.create_all(bind=engine)


# ✅ Provide a clean DB session per test
@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


# ✅ Provide a FastAPI test client with DB override
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides = {"get_db": override_get_db}
    with TestClient(app) as c:
        yield c
