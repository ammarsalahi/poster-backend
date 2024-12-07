from fastapi import APIRouter,Response,status,HTTPException
from pydantic.networks import EmailStr
from cruds import UserCrud,ValidationCrud
from models import *
from api import sessionDep
from core import create_access_token
from pydantic import EmailStr

routers=APIRouter()

routers.post("/signin",response_model=UserToken)
async def Signin(session:sessionDep,data:UserSignin):
    user=await UserCrud(session).read_for_sign(data)
    if user:
        token = create_access_token({"sub":user.username})
        return UserToken(access_token=token)


routers.post("/signup",response_model=UserToken)
async def Signup(db:sessionDep,data:UserAdd):
    user = await UserCrud(db).add(data)
    if user:
        token = create_access_token({"sub":user.username})
        return UserToken(access_token=token)

routers.post("/signout")
async def Signout():
    return {}


routers.post("/change_passowrd")
async def ChangePassowrd():
    return {}

routers.post("/email_validation")
async def EmailValid(db:sessionDep,data:ValidationAdd):
    user = await UserCrud(db).read_by_email(data.email)
    if user:
        valid = await ValidationCrud(db).add(data)
        return Response(status_code=status.HTTP_200_OK)

routers.post("/validation_check")
async def Verify(db:sessionDep,data:ValidationCheck):
    valid = await ValidationCrud(db).read_by_email(data.email)
    if valid.code != data.code :
        raise HTTPException(detail="Validation Check Error",status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_200_OK)
