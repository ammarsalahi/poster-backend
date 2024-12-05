from fastapi import APIRouter,status
from models import *
from api.deps import * 
from cruds import MediaCrud


routers=APIRouter()


@routers.get("/",response_model=List[MediaResponse])
async def list_medias(session:sessionDep,limit:int=10,offser:int=0):
    # use true for superuser before add token
    return await MediaCrud(session).read_all(limit,offset,True)

@routers.get("/{id}",response_model=MediaResponse)
async def detail_media(session:sessionDep,media_id:UUID):
    return await MediaCrud(session).read_one(media_id)

@routers.post("/",response_model=MediaResponse)
async def create_media(session:sessionDep,media_data:MediaAdd):
    return await MediaCrud(session).add(media_data)


@routers.patch("/{id}",response_model=MediaResponse)
async def update_media(session:sessionDep,media_id:UUID,media_data:MediaEdit):
    return await MediaCrud(session).update(media_id,media_data)


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(session:sessionDep,media_id:UUID):
    return await MediaCrud(session).delete(media_id)