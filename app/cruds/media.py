from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,or_
from fastapi import HTTPException,status
from models import *
from typing import List
from uuid import UUID


class MediaCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int,is_superuser:bool) -> List[Media]:
        if is_superuser:
            query=select(Media).offset(offset).limit(limit)
            async with self.db_session as session:
                medias = await session.execute(query)
                return medias.scalars()

    async def read_one(self,id:UUID) -> Media:
        query = select(Media).filter(Media.id == id)
        async with self.db_session as session:
            user=await session.execute(query)
            return user.scalar()

    async def add(self,media_data:MediaAdd) -> Media:
        media = Media(**media_data.dict())
        async with self.db_session as session:
            session.add(media)
            await session.commit()
        return media

    async def update(self,id:UUID,media_data:MediaEdit) -> Media:
        query = select(Media).filter(Media.id == id)
        try:
            async with self.db_session as session:
                media = session.execute(query)
                if media:
                    for key,value in media_data.dict(exclude_unset=True).items():
                        setattr(Media,key,value)
                        await session.commit()
                    return media
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
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
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
