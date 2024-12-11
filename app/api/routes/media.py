from fastapi import APIRouter,status,HTTPException
from schemas.media import *
from models import *
from api.deps import *
from cruds import MediaCrud
from schemas.response import *


routers=APIRouter()


@routers.get("/",response_model=List[MediaResponse])
async def list_medias(session:sessionDep,limit:int=10,offset:int=0):
    return await MediaCrud(session).read_all(limit,offset)


@routers.get("/{id}",response_model=MediaResponse)
async def detail_media(session:sessionDep,currentUser:userDep,media_id:UUID):
    if currentUser:
        return await MediaCrud(session).read_one(media_id)

@routers.post("/",response_model=MediaResponse)
async def create_media(session:sessionDep,currentUser:userDep,media_data:MediaAddSchema):
    if currentUser:
        return await MediaCrud(session).add(media_data)


@routers.patch("/{id}",response_model=MediaResponse)
async def update_media(session:sessionDep,currentUser:userDep,media_id:UUID,media_data:MediaEditSchema):
    media = await MediaCrud(session).read_one(media_id)
    if currentUser.is_superuser or currentUser.id==media.user_id:
        return await MediaCrud(session).update(media_id,media_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(session:sessionDep,currentUser:userDep,media_id:UUID):
    media = await MediaCrud(session).read_one(media_id)
    if currentUser.is_superuser or currentUser.id==media.user_id:
        return await MediaCrud(session).delete(media_id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
