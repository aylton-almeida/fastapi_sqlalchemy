import asyncio
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, String, Boolean, DateTime

Base = declarative_base()

class NoteBaseSchema(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    category: Optional[str] = None
    published: bool = False
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListNoteResponse(BaseModel):
    status: str
    results: int
    notes: List[NoteBaseSchema]


class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(String)
    published = Column(Boolean, default=False)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)


async def get_notes(session: AsyncSession) -> ListNoteResponse:
    result = await session.execute(select(Note))
    notes = result.scalars().all()
    return ListNoteResponse(status="success", results=len(notes), notes=notes)
