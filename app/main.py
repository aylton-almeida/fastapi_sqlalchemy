import asyncio
from app import models, note
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData

Base = declarative_base()
metadata = MetaData()

engine = create_async_engine("sqlite+aiomysql:///")
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note.router, tags=['Notes'], prefix='/api/notes')

@app.get("/api/healthchecker")
async def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}

@app.on_event("startup")
async def startup():
    await create_tables()

