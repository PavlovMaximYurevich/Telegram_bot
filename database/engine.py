import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base


engine = create_async_engine('sqlite+aiosqlite:///sqlite.db', echo=True)

sessionmaker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base.metadata.create_all(engine)


async def create_db():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)
