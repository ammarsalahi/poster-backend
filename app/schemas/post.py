from uuid import UUID
from fastapi import UploadFile
from typing_extensions import List
from pydantic import BaseModel



# class PostMediaAddSchema(BaseModel):
#     media_file:str

class PostAddSchema(BaseModel):
    content:str
    post_type:str
    user_id:UUID


class PostEditSchema(BaseModel):
    content:str|None=None
    post_type:str|None=None
    views:int|None=None
    visible:bool|None=None
