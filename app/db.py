"""Database session and engine setup using SQLAlchemy."""

import os
import sys

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(find_dotenv())

IS_TEST = 'pytest' in sys.modules

POSTGRES_DB = os.getenv('POSTGRES_TEST_DB') if IS_TEST else os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

DATABASE_URL = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
