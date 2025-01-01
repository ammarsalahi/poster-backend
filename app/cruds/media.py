from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.media import *
from app.models import *
from typing import List
from uuid import UUID
from app.schemas.response import *
import sqlalchemy as sql

class MediaCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(MediaModel).offset(offset).limit(limit)
        async with self.db_session as session:
            medias = await session.execute(query)
            return medias.scalars()

    async def read_one(self,id:UUID):
        query = sql.select(MediaModel).filter(MediaModel.id == id)
        async with self.db_session as session:
            try:
                media=await session.execute(query)
                return media.scalar_one()
            except sql.exc.NoResultFound:
                    raise HTTPException(detail="media Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,media_data:MediaAddSchema):
        media = MediaModel(**media_data.model_dump())
        async with self.db_session as session:
            try:
                session.add(media)
                await session.commit()
                return media
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,media_data:MediaEditSchema):
        query = sql.select(MediaModel).filter(MediaModel.id == id)
        try:
            async with self.db_session as session:
                result = await session.execute(query)
                media=result.scalar_one_or_none()
                for key,value in media_data.model_dump(exclude_unset=True).items():
                    setattr(media,key,value)
                    await session.commit()
                return media
        except sql.exc.NoResultFound:
                    raise HTTPException(detail="media Not Found!",status_code=status.HTTP_404_NOT_FOUND)        
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = sql.select(MediaModel).filter(MediaModel.id == id)
        async with self.db_session as session:
            try:
                media = session.execute(query)
                await session.delete(media)
                await session.commit()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="media Not Found!",status_code=status.HTTP_404_NOT_FOUND)
