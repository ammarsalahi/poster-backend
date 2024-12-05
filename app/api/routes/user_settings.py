from fastapi import APIRouter,status
from models import *
from api.deps import * 
from cruds import UserSettingsCrud


routers=APIRouter()


@routers.get("/",response_model=List[SettingsResponse])
async def list_settings(session:sessionDep,limit:int=10,offser:int=0):
    # use true for superuser before add token
    return await UserSettingsCrud(session).read_all(limit,offset,True)

@routers.get("/{id}",response_model=SettingsResponse)
async def detail_settings(session:sessionDep,sett_id:UUID):
    return await UserSettingsCrud(session).read_one(sett_id)

@routers.post("/",response_model=SettingsResponse)
async def create_settings(session:sessionDep,sett_data:SettingsAdd):
    return await UserSettingsCrud(session).add(sett_data)


@routers.patch("/{id}",response_model=SettingsResponse)
async def update_settings(session:sessionDep,sett_id:UUID,sett_data:SettingsEdit):
    return await UserSettingsCrud(session).update(sett_id,sett_data)


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_settings(session:sessionDep,sett_id:UUID):
    return await UserSettingsCrud(session).delete(sett_id)