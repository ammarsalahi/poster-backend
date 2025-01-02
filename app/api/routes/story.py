from fastapi import APIRouter,status,HTTPException,Form,File,UploadFile
from app.models import *
from app.api.deps import *
from app.cruds import StoryCrud
from app.schemas.response import *
from app.schemas.story import *
from app.utils.media import save_media

routers=APIRouter()


@routers.get("/",response_model=List[StoryResponse])
async def list_stories(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser:
        return await StoryCrud(session).read_all(limit,offset)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/info/{id}",response_model=StoryResponse)
async def detail_story(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser.is_superuser:
        return await StoryCrud(session).read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/{story_id}",response_model=StoryResponse)
async def detail_story_id(session:sessionDep,currentUser:userDep,story_id:str):
    if currentUser:
        return await StoryCrud(session).read_by_story_id(story_id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/user/",response_model=List[StoryResponse],description="get user stories")
async def detail_user_stories(session:sessionDep,currentUser:userDep):
    if currentUser:
        return await StoryCrud(session).read_by_user_id(currentUser.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.post("/",response_model=StoryOnlyResponse)
async def create_story(
    session:sessionDep,
    currentUser:userDep,
    story_type:str=Form(None),
    media_file:UploadFile=File(...)
):
    if currentUser:
        crud = StoryCrud(session)
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
        up_story = await crud.add(story_data)
        return await crud.read_one(up_story.id)


@routers.patch("/{id}",response_model=StoryOnlyResponse)
async def update_story(
    session:sessionDep,
    currentUser:userDep,
    id:str,
    story_type:str=Form(None),
    media_file:UploadFile=File(None)
):
    crud= StoryCrud(session)
    re_story=await crud.read_by_story_id(id)
    if currentUser.is_superuser or currentUser.id==re_story.user_id:
        if not media_file:
            raise HTTPException(
               status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No files were provided for upload."
            )
        file_str = await save_media(media_file)
        story_data = StoryEditSchema(
            story_type = story_type,
            media_file = file_str
        )
        up_story= await crud.update(re_story.id,story_data)
        return await crud.read_one(up_story.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(session:sessionDep,currentUser:userDep,id:str):
    story=await StoryCrud(session).read_by_story_id(id)
    if currentUser.is_superuser or currentUser.id==story.user_id:
        return await StoryCrud(session).delete(story.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.post("/like/")
async def add_like_story(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser:
        return await StoryCrud(session).like_story(id,currentUser.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.post("/unlike/")
async def remove_like_story(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser:
        return await StoryCrud(session).unlike_story(id,currentUser.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
