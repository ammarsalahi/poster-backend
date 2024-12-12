import os
from fastapi import UploadFile
from strawberry.file_uploads import Upload
from pathlib import Path
# Define base and media directories
BASE_DIR = Path(__file__).resolve().parent.parent  # Adjust to your project structure
MEDIA_DIR = BASE_DIR / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the `media` directory exists

async def save_media(mediafile: UploadFile) -> str:
    try:
        file_path :str = f"{MEDIA_DIR} / {mediafile.filename}"

        # Save the file
        with open(file_path, "wb") as buffer:
            buffer.write(await mediafile.read())

        # Return the file path as a string
        return str(file_path)
    except Exception as e:
        raise ValueError(f"Failed to save media: {e}")

async def save_graph_media(mediafile:Upload)->str:
    try:
        file_path:str= f"{MEDIA_DIR} / {mediafile.filename}"
        with open(file_path,"wb") as buffer:
            buffer.write(await mediafile.read())
        return file_path
    except Exception as e:
        raise ValueError(f"Failed to save media: {e}")
