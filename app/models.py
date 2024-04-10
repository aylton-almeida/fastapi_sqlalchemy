from .database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select

Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'
    id: Column = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    title: Column = Column(String, nullable=False)
    content: Column = Column(String, nullable=False)
    category: Column = Column(String, nullable=True)
    published: Column = Column(Boolean, nullable=False, default=True)
    createdAt: Column = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt: Column = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())

async def get_note(session: AsyncSession, note_id: GUID) -> Note:
    result = await session.execute(select(Note).where(Note.id == note_id))
    return result.scalars().first()

