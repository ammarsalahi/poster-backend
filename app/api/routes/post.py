from fastapi import APIRouter,status,HTTPException
from models import *
from api.deps import *
from cruds import PostCrud


routers=APIRouter()


@routers.get("/",response_model=List[PostResponse])
async def list_posts(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser:
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
async def create_post(session:sessionDep,currentUser:userDep,post_data:PostAdd):
    if currentUser:
        return await PostCrud(session).add(post_data)


@routers.patch("/{id}",response_model=PostResponse)
async def update_post(session:sessionDep,currentUser:userDep,post_id:str,post_data:PostEdit):
    post = await PostCrud(session).read_by_post_id(post_id)
    if currentUser.is_superuser or currentUser.id==post.user_id:
        return await PostCrud(session).update(post_id,post_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session:sessionDep,currentUser:userDep,id:UUID):
    post = await PostCrud(session).read_one(id)
    if currentUser.is_superuser or currentUser.id==post.user_id:
        return await PostCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
