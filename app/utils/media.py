import os
from fastapi import UploadFile
from strawberry.file_uploads import Upload


async def save_media(mediafile: UploadFile) -> str:
    try:
        # Define the upload directory
        upload_dir = "media"
        show_upload_dir="media"
        os.makedirs(name=upload_dir, exist_ok=True)

        # Generate a unique file name to prevent overwrites
        # unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(show_upload_dir, mediafile.filename)
        # Save the file
        with open(file_path, "wb") as buffer:
            buffer.write(await mediafile.read())
        print(file_path)
        return file_path
    except Exception as e:
        raise ValueError(f"Failed to save media: {e}")

async def save_graph_media(mediafile:Upload)->str:
    upload_dir="media"
    os.makedirs(name=upload_dir,exist_ok=True)
    file_path:str= os.path.join(upload_dir,mediafile.filename)
    with open(file_path,"wb") as buffer:
        buffer.write(await mediafile.read())
    return file_path
