from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,or_
from fastapi import HTTPException,status
from models import *
from typing import List
class UserSettingsCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int) -> List[SettingsResponse]:
        query=select(Settings).offset(offset).limit(limit)
        async with self.db_session as session:
            setts = await session.execute(query)
            return setts.scalars()

    async def read_one(self,id:UUID) -> SettingsResponse:
        query = select(Settings).filter(Settings.id==id)
        async with self.db_session as session:
            try:
                sett=await session.execute(query)
                if not sett:
                    raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return sett.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    async def read_by_user_id(self,user_id:UUID) -> SettingsResponse:
        query = select(Settings).filter(Settings.user_id==user_id)
        async with self.db_session as session:
            try:
                sett=await session.execute(query)
                if not sett:
                    raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return sett.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,set_data:SettingsAdd) -> SettingsResponse:
        sett = Settings(**set_data.dict())
        async with self.db_session as session:
            try:
                session.add(sett)
                await session.commit()
                return SettingsResponse(**sett.dict())
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,sett_data:SettingsEdit) -> SettingsResponse:
        query = select(Settings).filter(Settings.id == id)
        try:
            async with self.db_session as session:
                sett = await session.execute(query)
                if not sett:
                    raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)

                for key,value in sett_data.dict(exclude_unset=True).items():
                    setattr(Settings,key,value)
                    await session.commit()
                return sett.scalar_one()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = select(Settings).filter(Settings.id == id)
        async with self.db_session as session:
            sett = session.execute(query)
            if sett:
                await session.delete(sett)
                await session.commit()
            else:
                raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)
