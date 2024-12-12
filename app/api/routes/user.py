from fastapi import APIRouter,Depends,status,HTTPException,Form,File,UploadFile
from models import *
from typing import List,Annotated
from cruds import UserCrud
from api.deps import sessionDep,userDep
from schemas.response import *
from schemas.user import *
from utils.media import save_media


routers=APIRouter()


@routers.get("/",response_model=List[UserResponse])
async def list_users(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await UserCrud(session).read_all(limit=limit,offset=offset,is_superuser=currentUser.is_superuser)


# @routers.get("/details/{id}",response_model=User)
# async def detail_user_id(session:sessionDep,id:UUID):
#     return  await UserCrud(session).read_one(id)

@routers.get("/details",response_model=UserResponse)
async def detail_user(session:sessionDep,currentUser:userDep):
    return currentUser

@routers.get("/details/{username}",response_model=UserResponse)
async def detail_user_username(session:sessionDep,username:str):
    return  await UserCrud(session).read_by_username(username)

@routers.get("/search",response_model=List[UserOnlyResponse])
async def search_user(session:sessionDep,currentUser:userDep,query:str,limit:int=10):
    if currentUser:
        return  await UserCrud(session).filter(limit=limit,q=query)

@routers.post("/",response_model=UserOnlyResponse)
async def create_user(session:sessionDep,currentUser:userDep,user_data:UserAddAdminSchema):
    if currentUser.is_superuser:
        user=await UserCrud(session).add(user_data)
        return user

@routers.patch("/{id}",response_model=UserOnlyResponse)
async def update_user(
    session:sessionDep,
    currentUser:userDep,
    id:UUID,
    username:str = Form(None),
    fullname:str = Form(None),
    email:EmailStr = Form(None),
    profile_type:str = Form(None),
    profile_image:UploadFile = File(None),
    is_active:bool = Form(None),
    is_verified:bool = Form(None)
):
    if  currentUser.id==id:
        file_path=None
        if profile_image:
            file_path = await save_media(profile_image)
        user_data=UserEditSchema(
            username=username,
            fullname=fullname,
            email = email,
            profile_type= profile_type,
            profile_image = file_path,
            is_active = is_active,
            is_verified = is_verified
        )
        return await UserCrud(session).update(id,user_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.patch("/admin/{id}",response_model=UserOnlyResponse)
async def update_admin_user(
    session:sessionDep,
    currentUser:userDep,
    id:UUID,
    username:str = Form(None),
    fullname:str = Form(None),
    email:EmailStr = Form(None),
    profile_type:str = Form(None),
    profile_image:UploadFile = File(None),
    is_active:bool = Form(None),
    is_verified:bool = Form(None),
    is_superuser:bool = Form(None)
):
    if currentUser.is_superuser or currentUser.id==id:
        file_path=None
        if profile_image:
            file_path = await save_media(profile_image)
        user_data=UserEditAdminSchema(
            username=username,
            fullname=fullname,
            email = email,
            profile_type= profile_type,
            profile_image = file_path,
            is_active = is_active,
            is_verified = is_verified,
            is_superuser=is_superuser
        )
        return await UserCrud(session).update_admin(id,user_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser.id==id or currentUser.is_superuser:
        return await UserCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
