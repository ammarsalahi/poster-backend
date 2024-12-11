from fastapi import APIRouter,status,HTTPException
from models import *
from api.deps import *
from cruds import ValidationCrud
from pydantic import EmailStr
from schemas.response import *
from schemas.validation import *


routers=APIRouter()


@routers.get("/",response_model=List[ValidationResponse])
async def list_validations(session:sessionDep,currentUser:userDep,limit:int=10,offset:int=0):
    if currentUser.is_superuser:
        return await ValidationCrud(session).read_all(limit,offset)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/info/{id}",response_model=ValidationResponse)
async def detail_validation(session:sessionDep,currentUser:userDep,valid_id:UUID):
    if currentUser.is_superuser:
        return await ValidationCrud(session).read_one(valid_id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.get("/{email}",response_model=ValidationResponse)
async def detail_validation_email(session:sessionDep,currentUser:userDep,email:EmailStr):
    if currentUser:
        return await ValidationCrud(session).read_by_email(email)

@routers.post("/",response_model=ValidationResponse)
async def create_validation(session:sessionDep,valid_data:ValidationAddSchema):
    return await ValidationCrud(session).add(valid_data)

@routers.post('/verify')
async def validation_verify(session:sessionDep,valid_data:ValidationVerifySchema):
    return await ValidationCrud(session).read_verify(valid_data)



@routers.patch("/{id}",response_model=ValidationResponse)
async def update_validation(session:sessionDep,currentUser:userDep,valid_id:UUID,valid_data:ValidationEditSchema):
    if currentUser.is_superuser or valid_data.email:
        return await ValidationCrud(session).update(valid_id,valid_data)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_validation(session:sessionDep,currentUser:userDep,valid_id:UUID):
    if currentUser.is_superuser:
        return await ValidationCrud(session).delete(valid_id)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
