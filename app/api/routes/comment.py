from fastapi import APIRouter,status,HTTPException,Form
from app.models import *
from app.api.deps import *
from app.cruds import CommentCrud
from app.schemas.response import *
from app.schemas.comment import *
from uuid import UUID


routers=APIRouter()


@routers.get("/",response_model=List[CommentResponse])
async def list_comments(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await CommentCrud(session).read_all(limit,offset)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/{id}",response_model=CommentResponse)
async def detail_comment(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser:
        return await CommentCrud(session).read_one(id)

@routers.get("/user",response_model=List[CommentResponse])
async def detail_user_comment(session:sessionDep,currentUser:userDep):
    if currentUser:
        return await CommentCrud(session).read_by_user_id(currentUser.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.post("/",response_model=CommentOnlyResponse)
async def create_comment(
    session:sessionDep,
    currentUser:userDep,
    content:str=Form(),
    post_id:UUID=Form()
):
    if currentUser:
        crud = CommentCrud(session)
        data=CommentAddSchema(
            content=content,
            post_id=post_id,
            user_id=currentUser.id
        )
        cr_comment = await crud.add(data)
        return await crud.read_one(cr_comment.id)


@routers.patch("/{id}",response_model=CommentOnlyResponse)
async def update_comment(
    session:sessionDep,
    currentUser:userDep,
    id:UUID,
    content:str=Form()
):
    crud= CommentCrud(session)
    re_comment = await crud.read_one(id)
    if currentUser.is_superuser or currentUser.id==comment.user_id:
        comment_data=CommentEditSchema(content=content)
        up_comment = await crud.update(id,comment_data)
        return await crud.read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(session:sessionDep,currentUser:userDep,id:UUID):
    comment = await CommentCrud(session).read_one(id)
    if currentUser.is_superuser or currentUser.id==comment.user_id:
        return await CommentCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.post("/like")
async def add_like_comment(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser:
        return await CommentCrud(session).like_comment(id,currentUser.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.post("/unlike")
async def remove_like_comment(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser:
        return await CommentCrud(session).unlike_comment(id,currentUser.id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
