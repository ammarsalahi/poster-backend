from typing import Optional
from fastapi import APIRouter, File, Form, UploadFile,status,HTTPException
from schemas.media import MediaAddSchema
from schemas.comment import *
from schemas.post import *
from utils.media import save_media
from models import *
from api.deps import *
from cruds import PostCrud
from schemas.response import *


routers=APIRouter()


@routers.get("/",response_model=List[PostResponse])
async def list_posts(session:sessionDep,limit:int=10,offset:int=0):
    # if currentUser:
    return await PostCrud(session).read_all(limit,offset)


@routers.get("/info/{id}",response_model=PostResponse)
async def detail_post(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser.is_superuser:
        return await PostCrud(session).read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.get("/{post_id}",response_model=PostResponse)
async def detail_post_id(session:sessionDep,currentUser:userDep,post_id:str):
    if currentUser:
        return await PostCrud(session).read_by_post_id(post_id)

@routers.post("/",response_model=PostResponse)
async def create_post(
    session:sessionDep,
    currentUser:userDep,
    content:str=Form(),
    post_type:str=Form(None),
    upload_files:List[UploadFile]=File(...)
):
    if currentUser:
        crud=PostCrud(session)
        if not upload_files:
            raise HTTPException(
               status_code=400, detail="No files were provided for upload."
            )
        medias:List[str]=[]
        for upload in upload_files:
            file_path = await save_media(upload)
            medias.append(file_path)
        post_data=PostAddSchema(content=content,post_type=post_type,user_id=currentUser.id)
        post =await crud.add(post_data,medias)
        return await crud.read_one(post.id)



@routers.patch("/{id}",response_model=PostResponse)
async def update_post(
        session:sessionDep,
        currentUser:userDep,
        post_id:str,
        content:Optional[str]=Form(None),
        post_type:Optional[str]=Form(None),
        views:Optional[int]=Form(None),
        visible:Optional[bool]=Form(None),
        upload_files:List[UploadFile]=File(...)
):
    post = await PostCrud(session).read_by_post_id(post_id)
    if currentUser.is_superuser or currentUser.id==post.user_id:
        medias:List[str]=[]
        for upload in upload_files:
            file_path = await save_media(upload)
            medias.append(file_path)
        post= PostEditSchema(
            content=content,
            post_type=post_type,
            views=views,
            visible=visible
        )
        up_post=await PostCrud(session).update(post_id,post,medias)
        return post
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session:sessionDep,currentUser:userDep,id:UUID):
    post = await PostCrud(session).read_one(id)
    if currentUser.is_superuser or currentUser.id==post.user_id:
        return await PostCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
