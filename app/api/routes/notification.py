from typing import List
from fastapi import APIRouter,status,HTTPException
from app.api.deps import *
from app.cruds.notification import NotificationCrud
from app.schemas.notification import NotificationAddSchema, NotificationEditSchema
from app.schemas.response import NotificationResponse
from uuid import UUID


routers = APIRouter()


@routers.get("/",response_model=List[NotificationResponse])
async def list_notifies(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await NotificationCrud(session).read_all(limit,offset)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/{id}",response_model=NotificationResponse)
async def detail_notify(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser:
        return await NotificationCrud(session).read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.get("/user/",response_model=List[NotificationResponse],description="get user notifications")
async def detail_user_notify(session:sessionDep,currentUser:userDep):
    if currentUser:
        return await NotificationCrud(session).read_one(currentUser.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.post("/",response_model=NotificationResponse)
async def create_notify(session:sessionDep,currentUser:userDep,data:NotificationAddSchema):
    if currentUser:
        return await NotificationCrud(session).add(data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.patch("/{id}",response_model=NotificationResponse)
async def updae_notify(session:sessionDep,currentUser:userDep,id:UUID,data:NotificationEditSchema):
    notif= await NotificationCrud(session).read_one(id)
    if currentUser.id == notif.user_id or currentUser.is_superuser:
        return await NotificationCrud(session).update(id,data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session:sessionDep,currentUser:userDep,id:UUID):
    notif = await NotificationCrud(session).read_one(id)
    if currentUser.is_superuser or currentUser.id==notif.user_id:
        return await NotificationCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
