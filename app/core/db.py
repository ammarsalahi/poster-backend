from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from uuid import uuid4
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column,DateTime
import secrets
import string
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase
import asyncio


DATABASE_URL="sqlite+aiosqlite:///../data.sqlite"

engine=create_async_engine(
    url=DATABASE_URL
)

async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

class Base(DeclarativeBase):

    __abstract__=True

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid4,index=True,unique=True)
    created_at = Column(DateTime,default=func.now())
    updated_at = Column(DateTime,default=func.now(),onupdate=func.now())


async def get_db():
    db=async_session()
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


        
