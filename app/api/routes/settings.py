from fastapi import APIRouter,status,HTTPException
from app.models import *
from app.api.deps import *
from app.cruds import UserSettingsCrud
from app.schemas.response import *
from app.schemas.settings import *



routers=APIRouter()


@routers.get("/",response_model=List[SettingsResponse])
async def list_settings(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await UserSettingsCrud(session).read_all(limit,offset)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.get("/{id}",response_model=SettingsResponse)
async def detail_settings(session:sessionDep,currentUser:userDep,id:UUID):
    if currentUser.is_superuser:
        return await UserSettingsCrud(session).read_one(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

@routers.get("/detail",response_model=SettingsResponse)
async def detail_setting_user(session:sessionDep,currentUser:userDep):
    if currentUser:
        data = await UserSettingsCrud(session).read_by_user_id(currentUser.id)
        return data
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
    

@routers.post("/",response_model=SettingsResponse)
async def create_settings(session:sessionDep,currentUser:userDep,sett_data:SettingAddSchema):
    if currentUser:
        return await UserSettingsCrud(session).add(sett_data)

@routers.patch("/{id}",response_model=SettingsResponse)
async def update_settings(session:sessionDep,currentUser:userDep,id:UUID,sett_data:SettingEditSchema):
    sett = await UserSettingsCrud(session).read_one(id)
    if currentUser.is_superuser or currentUser.id==sett.user_id:
        return await UserSettingsCrud(session).update(id,sett_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_settings(session:sessionDep,currentUser:userDep,id:UUID):
    sett = await UserSettingsCrud(session).read_one(id)
    if currentUser.is_superuser or currentUser.id==sett.user_id:
        return await UserSettingsCrud(session).delete(id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
