from fastapi import APIRouter,Response,status,HTTPException
from pydantic.networks import EmailStr
from cruds import *
from models import *
from api import sessionDep
from core.token import create_access_token
from pydantic import EmailStr
from schemas.validation import *
from schemas.user import *

routers=APIRouter()



@routers.post("/signin",response_model=UserTokenSchema)
async def Signin(session:sessionDep,data:UserSignin):
    user=await UserCrud(session).read_for_sign(data)
    if user:
        token = create_access_token({"sub":user.username})
        return UserToken(access_token=token)


@routers.post("/signup",response_model=UserTokenSchema)
async def Signup(db:sessionDep,data:UserAddSchema):
    user = await UserCrud(db).add(data)
    if user:
        token = create_access_token({"sub":user.username})
        return UserToken(access_token=token)


@routers.post("/email_validation")
async def EmailValid(session:sessionDep,data:ValidationAddSchema):
    user = await UserCrud(db).read_by_email(data.email)
    if user:
        valid = await ValidationCrud(db).add(data)
        return Response(status_code=status.HTTP_200_OK)

@routers.post("/validation_check")
async def Verify(session:sessionDep,data:ValidationVerifySchema):
    return await ValidationCrud(session).read_verify(data)


@routers.post("/change_passowrd")
async def ChangePassowrd(session:sessionDep,):
    return {}