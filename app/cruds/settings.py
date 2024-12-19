from sqlalchemy.ext.asyncio.session import AsyncSession
import sqlalchemy as sql
from fastapi import HTTPException,status
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
        query = sql.select(Settings).filter(Settings.id==id)
        async with self.db_session as session:
            try:
                sett=await session.execute(query)
                if not sett:
                    raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return sett.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_user_id(self,user_id:UUID):
        query = sql.select(Settings).filter(Settings.user_id==user_id)
        async with self.db_session as session:
            try:
                sett=await session.execute(query)
                if not sett:
                    raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return sett.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,set_data:SettingAddSchema):
        sett = Settings(**set_data.dict())
        async with self.db_session as session:
            try:
                session.add(sett)
                await session.commit()
                return sett
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,sett_data:SettingEditSchema):
        query = sql.select(Settings).filter(Settings.id == id)
        try:
            async with self.db_session as session:
                result = await session.execute(query)
                sett = result.scalar_one_or_none()
                if not sett:
                    raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)

                for key,value in sett_data.dict(exclude_unset=True).items():
                    setattr(Settings,key,value)
                await session.commit()
                return sett
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = sql.select(Settings).filter(Settings.id == id)
        async with self.db_session as session:
            sett = session.execute(query)
            if sett:
                await session.delete(sett)
                await session.commit()
            else:
                raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)
