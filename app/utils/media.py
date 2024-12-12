from fastapi import UploadFile
from strawberry.file_uploads import Upload
from core.config import settings
import os


async def save_media(mediafile: UploadFile) -> str:
    try:
        media_path=f"./{settings.MEDIA_DIR}"
        file_path :str = os.path.join(media_path,mediafile.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await mediafile.read())
        return str(mediafile.filename)
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
