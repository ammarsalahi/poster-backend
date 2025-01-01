from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.notification import *
from app.models import *
from typing import List
from uuid import UUID
from app.schemas.response import *
import sqlalchemy as sql

class NotificationCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(NotificationModel).offset(offset).limit(limit)
        async with self.db_session as session:
            notifies = await session.execute(query)
            return notifies.scalars()

    async def read_one(self,id:UUID):
        query = sql.select(NotificationModel).filter(NotificationModel.id == id)
        async with self.db_session as session:
            try:
                notification=await session.execute(query)
                return notification.scalar_one()
            except sql.exc.NoResultFound:
                    raise HTTPException(detail="Notification Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_user_id(self,user_id:UUID):
        query = sql.select(NotificationModel).filter(NotificationModel.user_id == user_id)
        async with self.db_session as session:
            try:
                notification=await session.execute(query)
                return notification.scalars()
            except sql.exc.NoResultFound:
                    raise HTTPException(detail="Notification Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,notification_data:NotificationAddSchema):
        notification = NotificationModel(**notification_data.model_dump())
        async with self.db_session as session:
            try:
                session.add(notification)
                await session.commit()
                return notification
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,notification_data:NotificationEditSchema):
        query = sql.select(NotificationModel).filter(NotificationModel.id == id)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                notification=result.scalar_one_or_none()
                for key,value in notification_data.model_dump(exclude_unset=True).items():
                    setattr(notification,key,value)
                    await session.commit()
                return notification
            except sql.exc.NoResultFound:
                    raise HTTPException(detail="Notification Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = sql.select(NotificationModel).filter(NotificationModel.id == id)
        async with self.db_session as session:
            try:
                notification = session.execute(query)
                await session.delete(notification)
                await session.commit()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Message Not Found!",status_code=status.HTTP_404_NOT_FOUND)
