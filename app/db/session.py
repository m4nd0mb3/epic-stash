"""
Session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)

DATABASE_URL_TEST = "sqlite+aiosqlite:///memory?mode=memory&cache=shared&uri=true"
engine_test = create_async_engine(DATABASE_URL_TEST)
SessionLocalTest = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
