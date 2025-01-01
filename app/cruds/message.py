from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.message import *
from app.models import *
from typing import List
from uuid import UUID
from app.schemas.response import *
import sqlalchemy as sql

class MessageCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(MessageModel).offset(offset).limit(limit)
        async with self.db_session as session:
            messages = await session.execute(query)
            return messages.scalars()

    async def read_one(self,id:UUID):
        query = sql.select(MessageModel).filter(MessageModel.id == id)
        async with self.db_session as session:
            try:
                message=await session.execute(query)
                return message.scalar_one()
            except sql.exc.NoResultFound:
                    raise HTTPException(detail="Message Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_user_id(self,user_id:UUID):
        query = sql.select(MessageModel).filter(
            sql._or(
                MessageModel.send_user_id == user_id,
                MessageModel.recieve_user_id == user_id
            )
        )
        async with self.db_session as session:
            try:
                message=await session.execute(query)
                return message.scalars()
            except sql.exc.NoResultFound:
                    raise HTTPException(detail="Message Not Found!",status_code=status.HTTP_404_NOT_FOUND)    
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,message_data:MessageAddSchema):
        message = MessageModel(**message_data.model_dump())
        async with self.db_session as session:
            try:
                session.add(message)
                await session.commit()
                return message
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,message_data:MeessageEditSchema):
        query = sql.select(MessageModel).filter(MessageModel.id == id)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                message=result.scalar_one_or_none()
                for key,value in message_data.model_dump(exclude_unset=True).items():
                    setattr(message,key,value)
                    await session.commit()
                    return message
            except sql.exc.NoResultFound:
                    raise HTTPException(detail="Message Not Found!",status_code=status.HTTP_404_NOT_FOUND)        
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = sql.select(MessageModel).filter(MessageModel.id == id)
        async with self.db_session as session:
            try:
                message = session.execute(query)
                await session.delete(message)
                await session.commit()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Message Not Found!",status_code=status.HTTP_404_NOT_FOUND)
