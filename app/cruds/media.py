from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,or_
from fastapi import HTTPException,status
from models import *
from typing import List
from uuid import UUID


class MediaCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int) -> List[MediaResponse]:
        query=select(Media).offset(offset).limit(limit)
        async with self.db_session as session:
            medias = await session.execute(query)
            return medias.scalars()

    async def read_one(self,id:UUID) -> MediaResponse:
        query = select(Media).filter(Media.id == id)
        async with self.db_session as session:
            try:
                media=await session.execute(query)
                if not media:
                    raise HTTPException(detail="media Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return media.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,media_data:MediaAdd) -> MediaResponse:
        media = Media(**media_data.dict())
        async with self.db_session as session:
            try:
                session.add(media)
                await session.commit()
                return MediaResponse(**media.dict())
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,media_data:MediaEdit) -> MediaResponse:
        query = select(Media).filter(Media.id == id)
        try:
            async with self.db_session as session:
                media = await session.execute(query)
                if not media:
                    raise HTTPException(detail="media Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key,value in media_data.dict(exclude_unset=True).items():
                    setattr(Media,key,value)
                    await session.commit()
                return media.scalar_one()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = select(Media).filter(Media.id == id)
        async with self.db_session as session:
            media = session.execute(query)
            if media:
                await session.delete(media)
                await session.commit()
            else:
                raise HTTPException(detail="media Not Found!",status_code=status.HTTP_404_NOT_FOUND)
