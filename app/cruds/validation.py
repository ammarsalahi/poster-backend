from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select , or_,and_
from fastapi import HTTPException,status
from typing import List
from models import *
from pydantic import EmailStr


class ValidationCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int) -> List[ValidationResponse]:
        query=select(Validation).offset(offset).limit(limit)
        async with self.db_session as session:
            valids = await session.execute(query)
            return valids.scalars()

    async def read_one(self,id:UUID) -> ValidationResponse:
        query = select(Validation).filter(Validation.id==valid_id)
        async with self.db_session as session:
            try:
                valid=await session.execute(query)
                if not valid:
                    raise HTTPException(detail="Validation Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return valid.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_email(self,email:EmailStr) -> ValidationResponse:
        query = select(Validation).filter(Validation.email==email)
        async with self.db_session as session:
            try:
                valid=await session.execute(query)
                if not valid:
                    raise HTTPException(detail="Validation Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return valid.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,valid_data:ValidationAdd) -> Validation:
        valid = Validation(**valid_data.dict())
        async with self.db_session as session:
            try:
                session.add(valid)
                await session.commit()
                return valid
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,id:UUID,validation_data:ValidationEdit) -> ValidationResponse:
        query = select(Validation).filter(Validation.id == id)
        try:
            async with self.db_session as session:
                validation = await session.execute(query)
                if validation:
                    for key,value in validation_data.dict(exclude_unset=True).items():
                        setattr(validation,key,value)
                        await session.commit()
                    return ValidationResponse(**validation.dict())
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query = select(Validation).filter(Validation.id == id)
        async with self.db_session as session:
            valid = session.execute(query)
            if valid:
                await session.delete(valid)
                await session.commit()
            else:
                raise HTTPException(detail="Validation Not Found!",status_code=status.HTTP_404_NOT_FOUND)
