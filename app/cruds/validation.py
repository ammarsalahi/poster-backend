from sqlalchemy.ext.asyncio.session import AsyncSession
import sqlalchemy as sql 
from fastapi import HTTPException,status
from typing import List
from models import *
from pydantic import EmailStr
from schemas.response import *
from schemas.validation import *

class ValidationCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(ValidationModel).offset(offset).limit(limit)
        async with self.db_session as session:
            valids = await session.execute(query)
            return valids.scalars()

    async def read_one(self,id:UUID):
        query = sql.select(ValidationModel).filter(ValidationModel.id==valid_id)
        async with self.db_session as session:
            try:
                valid=await session.execute(query)
                if not valid:
                    raise HTTPException(detail="Validation Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return valid.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_email(self,email:EmailStr):
        query = sql.select(ValidationModel).filter(ValidationModel.email==str(email))
        async with self.db_session as session:
            try:
                valid=await session.execute(query)
                if not valid:
                    raise HTTPException(detail="Validation Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return valid.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    async def read_verify(self,valid_data:ValidationVerifySchema):
        query = sql.select(ValidationModel).filter(
            ValidationModel.email==str(email),
            ValidationModel.code==valid_data.code,
            ValidationModel.is_verified==False
        )
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                valid = result.scalar_one_or_none()
                if not valid:
                    raise HTTPException(detail="Validation Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                update_query = (sql.update(ValidationModel).where(
                    ValidationModel.email == str(valid_data.email),
                    ValidationModel.code == valid_data.code
                ).values(is_verified=True))

                await session.execute(update_query)
                await session.commit()
                return valid
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    async def add(self,valid_data:ValidationAdd):
        valid = ValidationModel(**valid_data.dict())
        async with self.db_session as session:
            try:
                session.add(valid)
                await session.commit()
                return valid
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,validation_data:ValidationEditSchema):
        query = sql.select(ValidationModel).filter(ValidationModel.id == id)
        try:
            async with self.db_session as session:
                result = await session.execute(query)
                validation = result.scalar_one_or_none()
                if validation:
                    for key,value in validation_data.dict(exclude_unset=True).items():
                        setattr(validation,key,value)
                    await session.commit()
                    return validation
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = sql.select(ValidationModel).filter(ValidationModel.id == id)
        async with self.db_session as session:
            valid = session.execute(query)
            if not valid:
                raise HTTPException(detail="Validation Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            await session.delete(valid)
            await session.commit()