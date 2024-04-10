import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

SQLITE_DATABASE_URL = "sqlite+aiomysql:///./note.db"

engine = create_async_engine(
    SQLITE_DATABASE_URL, echo=True
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> Session:
    async with async_session() as session:
        yield session
