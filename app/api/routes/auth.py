from fastapi import APIRouter,Response,status,HTTPException,Form,File,UploadFile,Request
from app.cruds import *
from app.models import *
from app.api.deps import sessionDep,userDep
from app.core.token import create_access_token
from pydantic import EmailStr
from app.schemas.validation import *
from app.schemas.user import *
from app.utils.media import save_media
from app.utils.oauth import google
from app.core.config import settings

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
async def ChangePassowrd(
    session:sessionDep,
    currentUser:userDep,
    currentPassword:str=Form(),
    newPassword:str=Form()
):
    if currentUser:
        data = UserPasswordChangeSchema(
            current_password=currentPassword,
            new_password=newPassword
        )
        return await UserCrud(session).change_password(currentUser.id,data)


@routers.get("/google")
async def google_login():
    return await google.authorize_redirect(request=None,redirect_uri=settings.GOOGLE_REDIRECT_URI)

@routers.get("/google/callback")
async def callback(request: Request):
    try:
        token = await google.authorize_access_token(request)
        user_info = await google.parse_id_token(request, token)
        return {"user": user_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
