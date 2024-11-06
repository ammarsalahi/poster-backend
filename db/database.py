from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,MappedAsDataclass

DATABASE_URL='sqlite+aiosqlite:///./data.db'

engine =create_async_engine(DATABASE_URL)
sessionLocal=async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

class Base(DeclarativeBase,MappedAsDataclass):
    pass

async def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        await db.close()
