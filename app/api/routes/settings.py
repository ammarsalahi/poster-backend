from fastapi import APIRouter,status,HTTPException
from models import *
from api.deps import *
from cruds import UserSettingsCrud
from schemas.response import *
from schemas.settings import *



routers=APIRouter()


@routers.get("/",response_model=List[SettingsResponse])
async def list_settings(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await UserSettingsCrud(session).read_all(limit,offset)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.get("/detail/{id}",response_model=SettingsResponse)
async def detail_settings(session:sessionDep,currentUser:userDep,sett_id:UUID):
    if currentUser.is_superuser:
        return await UserSettingsCrud(session).read_one(sett_id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.get("/detail",response_model=SettingsResponse)
async def detail_setting_user(session:sessionDep,currentUser:userDep,sett_id:UUID):
    return await UserSettingsCrud(session).read_by_user_id(currentUser.id)

@routers.post("/",response_model=SettingsResponse)
async def create_settings(session:sessionDep,currentUser:userDep,sett_data:SettingAddSchema):
    if currentUser:
        return await UserSettingsCrud(session).add(sett_data)

@routers.patch("/{id}",response_model=SettingsResponse)
async def update_settings(session:sessionDep,currentUser:userDep,sett_id:UUID,sett_data:SettingEditSchema):
    sett = await UserSettingsCrud(session).read_one(sett_id)
    if currentUser.is_superuser or currentUser.id==sett.user_id:
        return await UserSettingsCrud(session).update(sett_id,sett_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_settings(session:sessionDep,currentUser:userDep,sett_id:UUID):
    sett = await UserSettingsCrud(session).read_one(sett_id)
    if currentUser.is_superuser or currentUser.id==sett.user_id:
        return await UserSettingsCrud(session).delete(sett_id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
