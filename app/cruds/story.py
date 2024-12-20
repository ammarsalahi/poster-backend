from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List
from app.models import *
from fastapi import HTTPException,status
from app.schemas.response import *
import sqlalchemy as sql
from app.schemas.story import *
from sqlalchemy.orm import selectinload

class StoryCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(StoryModel).options(
            selectinload(StoryModel.liked_by)
        ).offset(offset).limit(limit)
        async with self.db_session as session:
            stories = await session.execute(query)
            return stories.unique().scalars()

    async def read_one(self,id:UUID):
        query = sql.select(StoryModel).options(
            selectinload(StoryModel.liked_by)
        ).filter(StoryModel.id==id)
        async with self.db_session as session:
            try:
                story=await session.execute(query)
                if not story:
                    raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return story.unique().scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




    async def read_by_story_id(self,story_id:str):
        query = sql.select(StoryModel).options(
            selectinload(StoryModel.liked_by)
        ).filter(StoryModel.story_id==story_id)
        async with self.db_session as session:
            try:
                story=await session.execute(query)
                if not story:
                    raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return story.unique().scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,story_data:StoryAddSchema):
        story = StoryModel(**story_data.dict())
        async with self.db_session as session:
            try:
                session.add(story)
                await session.commit()
                return story
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



    async def update(self,story_id:str,story_data:StoryEditSchema):
        query = sql.select(StoryModel).filter(StoryModel.story_id == story_id)
        try:
            async with self.db_session as session:
                result = await session.execute(query)
                story = result.scalar_one_or_none()
                if not story:
                    raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key,value in story_data.dict(exclude_unset=True).items():
                    setattr(story,key,value)
                await session.commit()
                return story
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = sql.select(StoryModel).filter(StoryModel.id == id)
        async with self.db_session as session:
            story = session.execute(query)
            if not story:
                raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)

            await session.delete(story)
            await session.commit()
