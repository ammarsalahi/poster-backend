from fastapi import UploadFile,Request
from strawberry.file_uploads import Upload
from app.core.config import settings
import os
from .uid_tool import get_uid
async def save_media(mediafile: UploadFile,request:Request) -> str:
    try:
        media_path=f"./{settings.MEDIA_DIR}"
        base_url = str(request.base_url).rstrip("/")
        newfilename = f"{get_uid(20)}_{mediafile.filename.replace(" ", "_")}"
        file_path :str = os.path.join(media_path,newfilename)
        with open(file_path, "wb") as buffer:
            buffer.write(await mediafile.read())
        return str(f"{base_url}/{settings.MEDIA_DIR}/{newfilename}")
    except Exception as e:
        raise ValueError(f"Failed to save media: {e}")


async def save_graph_media(mediafile:Upload)->str:
    try:
        file_path:str= f"./{settings.MEDIA_DIR}/{mediafile.filename}"
        with open(file_path,"wb") as buffer:
            buffer.write(await mediafile.read())
        return file_path
    except Exception as e:
        raise ValueError(f"Failed to save media: {e}")
