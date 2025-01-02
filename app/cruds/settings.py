from sqlalchemy.ext.asyncio.session import AsyncSession
import sqlalchemy as sql
from fastapi import HTTPException,status,Response
from app.models import *
from typing import List
from app.schemas.response import *
from app.schemas.settings import *

class UserSettingsCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(SettingsModel).offset(offset).limit(limit)
        async with self.db_session as session:
            setts = await session.execute(query)
            return setts.scalars()

    async def read_one(self,id:UUID):
        query = sql.select(SettingsModel).filter(SettingsModel.id==id)
        async with self.db_session as session:
            try:
                sett=await session.execute(query)
                return sett.scalar_one()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_user_id(self,user_id:UUID):
        query = sql.select(SettingsModel).filter(SettingsModel.user_id==user_id)
        async with self.db_session as session:
            try:
                sett=await session.execute(query)
                return sett.scalar_one()
            except  sql.exc.NoResultFound:
                raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,set_data:SettingAddSchema):
        sett = SettingsModel(**set_data.model_dump())
        async with self.db_session as session:
            try:
                session.add(sett)
                await session.commit()
                return sett
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,sett_data:SettingEditSchema):
        query = sql.select(SettingsModel).filter(SettingsModel.id == id)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                sett = result.scalar_one_or_none()
                for key,value in sett_data.model_dump(exclude_unset=True).items():
                    setattr(SettingsModel,key,value)
                await session.commit()
                return sett
            except  sql.exc.NoResultFound:
                raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = sql.select(SettingsModel).filter(SettingsModel.id == id)
        async with self.db_session as session:
            try:
                result = session.execute(query)
                sett = result.scalar_one_or_none()
                if not sett:
                    raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
                await session.delete(sett)
                await session.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT,content="settings delete successfully.")
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)
