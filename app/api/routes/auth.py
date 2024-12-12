from fastapi import APIRouter,Response,status,HTTPException,Form,File,UploadFile
from cruds import *
from models import *
from api.deps import sessionDep
from core.token import create_access_token
from pydantic import EmailStr
from schemas.validation import *
from schemas.user import *
from utils.media import save_media
routers=APIRouter()



@routers.post("/signin",response_model=UserTokenSchema)
async def Signin(session:sessionDep,username:str=Form(),password:str=Form()):
    data=UserSigninSchema(
        username=username,
        password=password
    )
    user=await UserCrud(session).read_for_sign(data)
    if user:
        token = create_access_token({"sub":user.username})
        return UserTokenSchema(access_token=token)


@routers.post("/signup",response_model=UserTokenSchema)
async def Signup(
    session:sessionDep,
    fullname:str=Form(),
    username:str=Form(),
    email:EmailStr=Form(),
    password:str = Form(),
    profile_type:str=Form(None),
    profile_image:UploadFile|None=File(None)
):
    file_path=None
    print(profile_image)
    if profile_image is not None:
        file_path = await save_media(profile_image)
    data=UserAddSchema(
        fullname=fullname,
        username=username,
        email=email,
        password=password,
        profile_type=profile_type,
        profile_image=file_path
    )
    user = await UserCrud(session).add(data)
    if user:
        token = create_access_token({"sub":user.username})
        return UserTokenSchema(access_token=token)


@routers.post("/email_validation")
async def EmailValid(session:sessionDep,data:ValidationAddSchema):
    user = await UserCrud(session).read_by_email(data.email)
    if user:
        valid = await ValidationCrud(session).add(data)
        return Response(status_code=status.HTTP_200_OK)

@routers.post("/validation_check")
async def Verify(session:sessionDep,data:ValidationVerifySchema):
    valid = await ValidationCrud(session).read_verify(data)
    if valid:
        token = create_access_token({"sub":valid.email})
        return UserTokenSchema(access_token=token)



@routers.post("/change_passowrd")
async def ChangePassowrd(session:sessionDep,):
    return {}
