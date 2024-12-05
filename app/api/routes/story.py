from fastapi import APIRouter,status
from models import *
from api.deps import * 
from cruds import StoryCrud


routers=APIRouter()


@routers.get("/",response_model=List[StoryResponse])
async def list_stories(session:sessionDep,limit:int=10,offser:int=0):
    return await StoryCrud(session).read_all(limit,offset)



@routers.get("/info/{id}",response_model=StoryResponse)
async def detail_story(session:sessionDep,id:UUID):
    return await StoryCrud(session).read_one(story_id)

@routers.get("/{id}",response_model=StoryResponse)
async def detail_story(session:sessionDep,story_id:str):
    return await StoryCrud(session).read_by_story_id(story_id)

@routers.post("/",response_model=StoryResponse)
async def create_story(session:sessionDep,story_data:StoryAdd):
    return await StoryCrud(session).add(story_data)


@routers.patch("/{id}",response_model=StoryResponse)
async def update_story(session:sessionDep,story_id:str,story_data:StoryEdit):
    return await StoryCrud(session).update(story_id,story_data)


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(session:sessionDep,story_id:UUID):
    return await StoryCrud(session).delete(story_id)
          
