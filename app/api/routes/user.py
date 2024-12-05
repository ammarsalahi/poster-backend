from fastapi import APIRouter,Depends,status
from models import *
from typing import List,Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from cruds import UserCrud
from api.deps import sessionDep


routers=APIRouter()


@routers.get("/",response_model=List[UserResponse])
async def list_users(session:sessionDep,limit:int=10,offset:int=0):
    return await UserCrud(session).read_all(limit=limit,offset=offset,is_superuser=True)


@routers.get("/info/{id}",response_model=User)
async def info_user(session:sessionDep,id:UUID):
    return  await UserCrud(session).read_one(id)

@routers.get("/{username}",response_model=UserResponse)
async def detail_user(session:sessionDep,username:str):
    return  await UserCrud(session).read_by_username(username)

@routers.post("/",response_model=User)
async def create_user(session:sessionDep,user_data:UserAdd):
    user=await UserCrud(session).add(user_data)
    return user

@routers.patch("/{id}",response_model=UserResponse)
async def update_user(session:sessionDep,id:UUID,user_data:UserEdit):
    user = await UserCrud(session).update(id,user_data)
    return user

@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session:sessionDep,id:UUID):
    return await UserCrud(session).delete(id)
