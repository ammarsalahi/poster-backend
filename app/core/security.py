from datetime import timedelta,timezone,datetime
from fastapi import HTTPException,status,Depends
import jwt
import secrets
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from sqlalchemy.orm.mapper import reconstructor
from cruds import UserCrud
from api import sessionDep
from passlib.context import CryptContext


SECRET_KEY=secrets.token_hex(62)
ALGORITHM = "HS256"
EXPIRE_TIME_DELTA=24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/signin")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=EXPIRE_TIME_DELTA)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db:sessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await UserCrud(db).read_by_username(username)
    if user is None:
        raise credentials_exception
    return user

def hashed_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)
