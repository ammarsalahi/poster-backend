from fastapi import APIRouter,status,HTTPException,Form,File,UploadFile
from models import *
from api.deps import *
from cruds import StoryCrud
from schemas.response import *
from schemas.story import *
from utils.media import save_media

routers=APIRouter()


@routers.get("/",response_model=List[StoryResponse])
async def list_stories(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser:
        return await StoryCrud(session).read_all(limit,offset)


@routers.get("/info/{id}",response_model=StoryResponse)
async def detail_story(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser.is_superuser:
        return await StoryCrud(session).read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/{story_id}",response_model=StoryResponse)
async def detail_story_id(session:sessionDep,currentUser:userDep,story_id:str):
    if currentUser:
        return await StoryCrud(session).read_by_story_id(story_id)

@routers.post("/",response_model=StoryOnlyResponse)
async def create_story(
    session:sessionDep,
    currentUser:userDep,
    story_type:str=Form(None),
    media_file:UploadFile=File(...)
):
    if currentUser:
        if not media_file:
            raise HTTPException(
               status_code=400, detail="No files were provided for upload."
            )
        file_str = await save_media(media_file)
        story_data = StoryAddSchema(
            story_type = story_type,
            user_id=currentUser.id,
            media_file = file_str
        )
        return await StoryCrud(session).add(story_data)


@routers.patch("/{id}",response_model=StoryOnlyResponse)
async def update_story(
    session:sessionDep,
    currentUser:userDep,
    id:str,
    story_type:str=Form(None),
    media_file:UploadFile=File(None)
):
    story=await StoryCrud(session).read_by_story_id(id)
    if currentUser.is_superuser or currentUser.id==story.user_id:
        if not media_file:
            raise HTTPException(
               status_code=400, detail="No files were provided for upload."
            )
        file_str = await save_media(media_file)
        story_data = StoryEditSchema(
            story_type = story_type,
            media_file = file_str
        )
        return await StoryCrud(session).update(id,story_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(session:sessionDep,currentUser:userDep,id:UUID):
    story=await StoryCrud(session).read_one(id)
    if currentUser.is_superuser or currentUser.id==story.user_id:
        return await StoryCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
