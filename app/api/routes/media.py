from fastapi import APIRouter,status,HTTPException,File,UploadFile,Form
from app.schemas.media import *
from app.models import *
from app.api.deps import *
from app.cruds import MediaCrud
from app.schemas.response import *
from app.utils.media import save_media

routers=APIRouter()


@routers.get("/",response_model=List[MediaResponse])
async def list_medias(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await MediaCrud(session).read_all(limit,offset)


@routers.get("/{id}",response_model=MediaResponse)
async def detail_media(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser:
        return await MediaCrud(session).read_one(id)

@routers.post("/",response_model=MediaResponse)
async def create_media(session:sessionDep,currentUser:userDep,media_file:UploadFile=File(...),post_id:UUID=Form()):
    if currentUser:
        if not media_file:
            raise HTTPException(
               status_code=400, detail="No file were provided for upload."
            )

        file_path=await save_media(media_file)
        media_data=MediaAddSchema(
            media_file= file_path,
            post_id=post_id
        )
        return await MediaCrud(session).add(media_data)


@routers.patch("/{id}",response_model=MediaResponse)
async def update_media(session:sessionDep,currentUser:userDep,id:UUID,media_file:UploadFile=File(...),):
    crud = MediaCrud(session)
    media = await crud.read_one(id)
    if currentUser:
        if not media_file:
            raise HTTPException(
               status_code=400, detail="No file were provided for upload."
            )

        file_path=await save_media(media_file)
        media_data=MediaEditSchema(
            media_file= file_path
        )
        up_media = await crud.update(id,media_data)
        return await crud.read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(session:sessionDep,currentUser:userDep,id:UUID):
    media = await MediaCrud(session).read_one(id)
    if currentUser:
        return await MediaCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
