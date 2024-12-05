from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select , or_
from typing import List
from models import *
class StoryCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int,is_superuser:bool) -> List[Story]:
        if is_superuser:
            query=select(Story).offset(offset).limit(limit)
            async with self.db_session as session:
                stories = await session.execute(query)
                return stories.scalars()

    async def read_one(self,id:UUID) -> Story:
        query = select(Story).filter(Story.id==story_id)
        async with self.db_session as session:
            story=await session.execute(query)
            return story.scalar()

    async def read_by_story_id(self,story_id:str) -> Story:
        query = select(Story).filter(Story.story_id==story_id)
        async with self.db_session as session:
            story=await session.execute(query)
            return story.scalar()

    async def add(self,Story_data:StoryAdd) -> Story:
        story = Story(**story_data.dict())
        async with self.db_session as session:
            session.add(story)
            await session.commit()
        return story

    async def update(self,id:UUID,story_data:StoryEdit) -> Story:
        query = select(Story).filter(Story.id == id)
        try:
            async with self.db_session as session:
                Story = session.execute(query)
                if Story:
                    for key,value in Story_data.dict(exclude_unset=True).items():
                        setattr(Story,key,value)
                        await session.commit()
                    return Story
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
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
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
