from core import async_session_factory
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from typing import Annotated

async def get_db():
    async with async_session_factory() as session:
        yield session

sessionDep = Annotated[AsyncSession,Depends(get_db)]
