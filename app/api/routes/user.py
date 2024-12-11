from fastapi import APIRouter,Depends,status,HTTPException
from models import *
from typing import List,Annotated
from cruds import UserCrud
from api.deps import sessionDep,userDep
from schemas.response import *
from schemas.user import *


routers=APIRouter()


@routers.get("/",response_model=List[UserResponse])
async def list_users(session:sessionDep,limit:int=10,offset:int=0):
    return await UserCrud(session).read_all(limit=limit,offset=offset,is_superuser=True)


# @routers.get("/details/{id}",response_model=User)
# async def detail_user_id(session:sessionDep,id:UUID):
#     return  await UserCrud(session).read_one(id)

@routers.get("/details",response_model=UserResponse)
async def detail_user(session:sessionDep,currentUser:userDep):
    return currentUser

@routers.get("/details/{username}",response_model=UserResponse)
async def detail_user_username(session:sessionDep,username:str):
    return  await UserCrud(session).read_by_username(username)

@routers.get("/search",response_model=List[UserOnlyResponse])
async def search_user(session:sessionDep,currentUser:userDep,query:str,limit:int=10):
    if currentUser:
        return  await UserCrud(session).filter(limit=limit,q=query)

@routers.post("/",response_model=UserOnlyResponse)
async def create_user(session:sessionDep,user_data:UserAdd):
    user=await UserCrud(session).add(user_data)
    return user

@routers.patch("/{id}",response_model=UserOnlyResponse)
async def update_user(session:sessionDep,currentUser:userDep,id:UUID,user_data:UserEdit):
    if currentUser.is_superuser or currentUser.id==id:
        return await UserCrud(session).update(id,user_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser.id==id or currentUser.is_superuser:
        return await UserCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
