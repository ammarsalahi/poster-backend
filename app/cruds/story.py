from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select , or_
from typing import List
from models import *
from fastapi import HTTPException,status
class StoryCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int) -> List[StoryResponse]:
        query=select(Story).offset(offset).limit(limit)
        async with self.db_session as session:
            stories = await session.execute(query)
            return stories.scalars()

    async def read_one(self,id:UUID) -> Story:
        query = select(Story).filter(Story.id==id)
        async with self.db_session as session:
            try:
                story=await session.execute(query)
                if not story:
                    raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return story.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




    async def read_by_story_id(self,story_id:str) -> StoryResponse:
        query = select(Story).filter(Story.story_id==story_id)
        async with self.db_session as session:
            try:
                story=await session.execute(query)
                if not story:
                    raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return story.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,story_data:StoryAdd) -> StoryResponse:
        story = Story(**story_data.dict())
        async with self.db_session as session:
            session.add(story)
            await session.commit()
        return StoryResponse(**story.dict())

    async def update(self,story_id:str,story_data:StoryEdit) -> StoryResponse:
        query = select(Story).filter(Story.story_id == story_id)
        try:
            async with self.db_session as session:
                story = await session.execute(query)
                if not story:
                    raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key,value in story_data.dict(exclude_unset=True).items():
                    setattr(story,key,value)
                    await session.commit()
                return story.scalar_one()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = select(Story).filter(Story.id == id)
        async with self.db_session as session:
            story = session.execute(query)
            if story:
                await session.delete(story)
                await session.commit()
            else:
                raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
