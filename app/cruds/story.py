from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List
from app.models import *
from fastapi import HTTPException,status,Response
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
            return stories.unique().scalars().all()

    async def read_one(self,id:UUID):
        query = sql.select(StoryModel).options(
            selectinload(StoryModel.liked_by)
        ).filter(StoryModel.id==id)
        async with self.db_session as session:
            try:
                story=await session.execute(query)
                return story.unique().scalar_one()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




    async def read_by_story_id(self,story_id:str):
        query = sql.select(StoryModel).options(
            selectinload(StoryModel.liked_by)
        ).filter(StoryModel.story_id==story_id)
        async with self.db_session as session:
            try:
                story=await session.execute(query)
                return story.unique().scalar_one()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_user_id(self,user_id:UUID):
        query = sql.select(StoryModel).options(
            selectinload(StoryModel.liked_by)
        ).filter(StoryModel.user_id==user_id)
        async with self.db_session as session:
            try:
                story=await session.execute(query)
                return story.unique().scalars()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    async def add(self,story_data:StoryAddSchema):
        story = StoryModel(**story_data.model_dump())
        async with self.db_session as session:
            try:
                session.add(story)
                await session.commit()
                return story
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



    async def update(self,id:UUID,story_data:StoryEditSchema):
        query = sql.select(StoryModel).filter(StoryModel.id == id)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                story = result.scalar_one_or_none()
                if not story:
                    raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key,value in story_data.model_dump(exclude_unset=True).items():
                    if value is not None:
                        setattr(story,key,value)
                await session.commit()
                return story
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = sql.select(StoryModel).filter(StoryModel.id == id)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                story = result.scalar_one_or_none()
                if not story:
                    raise HTTPException(detail="Settings Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
                await session.delete(story)
                await session.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT,content="stroy delete successfully.")
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Story Not Found!",status_code=status.HTTP_404_NOT_FOUND)
    

    async def like_story(self,story_id:UUID,user_id:UUID):
        story_query = sql.select(StoryModel).filter(StoryModel.id==story_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                story_result= await session.execute(story_query)
                user_result= await session.execute(user_query)

                story = story_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not story:
                    raise HTTPException(detail="Stroy Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                story.liked_by.append(user)
                await session.commit()
                return {"message":"story liked successfully!"}
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def unlike_story(self,story_id:UUID,user_id:UUID):
        story_query = sql.select(StoryModel).filter(StoryModel.id==story_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                story_result= await session.execute(story_query)
                user_result= await session.execute(user_query)

                story = story_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not story:
                    raise HTTPException(detail="Stroy Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                story.liked_by.remove(user)
                await session.commit()
                return {"message":"story liked successfully!"}
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def save_story(self,story_id:UUID,user_id:UUID):
        story_query = sql.select(StoryModel).filter(StoryModel.id==story_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                story_result= await session.execute(story_query)
                user_result= await session.execute(user_query)

                story = story_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not story:
                    raise HTTPException(detail="Stroy Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                story.saved_by.append(user)
                await session.commit()
                return {"message":"story saved successfully!"}
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def unsave_story(self,story_id:UUID,user_id:UUID):
        story_query = sql.select(StoryModel).filter(StoryModel.id==story_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                story_result= await session.execute(story_query)
                user_result= await session.execute(user_query)

                story = story_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not story:
                    raise HTTPException(detail="Stroy Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                story.saved_by.remove(user)
                await session.commit()
                return {"message":"story unsaved successfully!"}
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)                