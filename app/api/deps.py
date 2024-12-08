from core import get_db
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends,HTTPException,status
from typing import Annotated
from models import UserResponse
from tokens import get_current_user



sessionDep = Annotated[AsyncSession,Depends(get_db)]

userDep = Annotated[UserResponse,Depends(get_current_user)]
