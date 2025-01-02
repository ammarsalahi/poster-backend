from typing import List
from fastapi import APIRouter,status,HTTPException
from app.api.deps import *
from app.cruds.message import  MessageCrud
from app.schemas.message import *
from app.schemas.response import MessageResponse
from uuid import UUID


routers = APIRouter()


@routers.get("/",response_model=List[MessageResponse])
async def list_messages(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await MessageCrud(session).read_all(limit,offset)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/{id}",response_model=MessageResponse)
async def detail_message(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser:
        return await MessageCrud(session).read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/user",response_model=List[MessageResponse],description="get user messages")
async def detail_user_message(session:sessionDep,currentUser:userDep):
    if currentUser:
        return await MessageCrud(session).read_one(currentUser.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.post("/",response_model=MessageResponse)
async def create_message(session:sessionDep,currentUser:userDep,data:MessageAddSchema):
    if currentUser:
        crud = MessageCrud(session)
        cr_message = await crud.add(data)
        return await crud.read_one(cr_message.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.patch("/{id}",response_model=MessageResponse)
async def update_message(session:sessionDep,currentUser:userDep,id:UUID,data:MeessageEditSchema):
    crud = MessageCrud(session)
    message= crud.read_one(id)
    if currentUser.id == message.send_user_id or currentUser.is_superuser:
        
        up_message = await crud.update(id,data)
        return await crud.read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session:sessionDep,currentUser:userDep,id:UUID):
    message = await MessageCrud(session).read_one(id)
    if currentUser.is_superuser or currentUser.id==message.send_user_id:
        return await MessageCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
