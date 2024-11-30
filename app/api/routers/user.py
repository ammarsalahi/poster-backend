from fastapi import APIRouter,Depends
from models import User,UserCreate
from typing import List,Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from db import get_db
from cruds import UserCrud

routers=APIRouter()


db_dependency = Annotated[AsyncSession,Depends(get_db)]

@routers.get("/",response_model=List[User])
async def list_users(session:db_dependency,limit:int=10,offset:int=0):
    
    return await UserCrud(db_session=session).read_all(limit=limit,offset=offset,is_superuser=True)
    

@routers.get("/{id}")
async def detail_user():
    return {}

@routers.post("/",response_model=User)
async def create_user(db:db_dependency,user_data:UserCreate):
    crud=UserCrud(db)
    user=await UserCrud(db).add(user_data)
    return user

@routers.patch("/{id}")
async def update_user():
    return {}

@routers.delete("/{id}")
async def delete_user():
    return {}            
