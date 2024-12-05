from fastapi import APIRouter,status
from models import *
from api.deps import * 
from cruds import CommentCrud


routers=APIRouter()


@routers.get("/",response_model=List[CommentResponse])
async def list_comments(session:sessionDep,limit:int=10,offser:int=0):
    # use true for superuser before add token
    return await CommentCrud(session).read_all(limit,offset,True)



@routers.get("/{id}",response_model=CommentResponse)
async def detail_comment(session:sessionDep,comment_id:UUID):
    return await CommentCrud(session).read_one(comment_id)

@routers.post("/",response_model=CommentResponse)
async def create_comment(session:sessionDep,comment_data:CommentAdd):
    return await CommentCrud(session).add(comment_data)


@routers.patch("/{id}",response_model=CommentResponse)
async def update_comment(session:sessionDep,comment_id:UUID,comment_data:CommentEdit):
    return await CommentCrud(session).update(comment_id,comment_data)


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(session:sessionDep,comment_id:UUID):
    return await CommentCrud(session).delete(comment_id)
