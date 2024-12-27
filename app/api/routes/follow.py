from fastapi import APIRouter,Response,status,HTTPException
from app.schemas.follow import *
from app.cruds import FollowCrud
from app.api.deps import *
from uuid import UUID


routers = APIRouter()

@routers.get("/")
async def list_follow(db:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await FollowCrud(db).read_all(limit,offset)

@routers.get("/{id}")
async def details(db:sessionDep,currentUser:userDep,id:UUID):
    if currentUser.is_superuser:
        return await FollowCrud(db).read_one(id)


@routers.post("/add",status_code=status.HTTP_200_OK)
async def follow_user(db:sessionDep,currentUser:userDep,data:FollowSchema):
    if currentUser:
        return await FollowCrud(db).add(data)


@routers.post("/remove",status_code=status.HTTP_200_OK)
async def unfollow_user(db:sessionDep,currentUser:userDep,data:FollowSchema):
    if currentUser:
        return await FollowCrud(db).remove(data)
