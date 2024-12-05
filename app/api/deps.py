from core import async_session_factory
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends,HTTPException
from typing import Annotated
from models import UserResponse
from core import get_current_user



async def get_db():
    async with async_session_factory() as session:
        yield session

sessionDep = Annotated[AsyncSession,Depends(get_db)]

userDep = Annotated[UserResponse,Depends(get_current_user)]
