from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    DateTime,
    func,
    UUID
)
from uuid import uuid4

DATABASE_URL='sqlite+aiosqlite:///./data.db'

engine =create_async_engine(DATABASE_URL)

sessionLocal=async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    __abstract_=True

    id = Column(UUID(as_uuid=uuid4),primary_key=True,default=uuid4,index=True,unique=True)
    created_at = Column(DateTime,default=func.now())
    updated_at = Column(DateTime,default=func.now(),onupdate=func.now())
async def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        await db.close()
