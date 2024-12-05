from fastapi import APIRouter,status
from models import *
from api.deps import * 
from cruds import PostCrud


routers=APIRouter()


@routers.get("/",response_model=List[PostResponse])
async def list_posts(session:sessionDep,limit:int=10,offser:int=0):
    # use true for superuser before add token
    return await PostCrud(session).read_all(limit,offset)



@routers.get("/info/{id}",response_model=PostResponse)
async def detail_post(session:sessionDep,id:UUID):
    return await PostCrud(session).read_one(post_id)

@routers.get("/{id}",response_model=PostResponse)
async def detail_post(session:sessionDep,post_id:str):
    return await PostCrud(session).read_by_post_id(post_id)

@routers.post("/",response_model=PostResponse)
async def create_post(session:sessionDep,post_data:CommentAdd):
    return await PostCrud(session).add(post_data)


@routers.patch("/{id}",response_model=PostResponse)
async def update_post(session:sessionDep,post_id:str,post_data:PostEdit):
    return await PostCrud(session).update(post_id,post_data)


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session:sessionDep,post_id:UUID):
    return await PostCrud(session).delete(post_id)
          
