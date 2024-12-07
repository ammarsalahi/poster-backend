from fastapi import APIRouter,status,HTTPException
from models import *
from api.deps import *
from cruds import CommentCrud


routers=APIRouter()


@routers.get("/",response_model=List[CommentResponse])
async def list_comments(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await CommentCrud(session).read_all(limit,offset)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/{id}",response_model=CommentResponse)
async def detail_comment(session:sessionDep,currentUser:userDep,comment_id:UUID):
    if currentUser:
        return await CommentCrud(session).read_one(comment_id)

@routers.post("/",response_model=CommentResponse)
async def create_comment(session:sessionDep,currentUser:userDep,comment_data:CommentAdd):
    if currentUser:
        return await CommentCrud(session).add(comment_data)


@routers.patch("/{id}",response_model=CommentResponse)
async def update_comment(session:sessionDep,currentUser:userDep,comment_id:UUID,comment_data:CommentEdit):
    comment = await CommentCrud(session).read_one(comment_id)
    if currentUser.is_superuser or currentUser.id==comment.user_id:
        return await CommentCrud(session).update(comment_id,comment_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(session:sessionDep,currentUser:userDep,comment_id:UUID):
    comment = await CommentCrud(session).read_one(comment_id)
    if currentUser.is_superuser or currentUser.id==comment.user_id:
        return await CommentCrud(session).delete(comment_id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
