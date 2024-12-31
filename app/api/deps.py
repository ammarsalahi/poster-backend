from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core import get_db
from fastapi import Depends,HTTPException,status
from typing import Annotated
from app.schemas.response import *
from app.core.token import get_current_user


sessionDep = Annotated[AsyncSession,Depends(get_db)]
userDep = Annotated[UserOnlyResponse,Depends(get_current_user)]
