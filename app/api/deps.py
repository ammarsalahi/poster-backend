from sqlalchemy.ext.asyncio.session import AsyncSession
from core import get_db
from fastapi import Depends,HTTPException,status
from typing import Annotated
from schemas.response import *
from core.token import get_current_user


sessionDep = Annotated[AsyncSession,Depends(get_db)]
userDep = Annotated[UserResponse,Depends(get_current_user)]
