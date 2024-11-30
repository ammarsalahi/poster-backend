from fastapi import APIRouter

routers=APIRouter()


@routers.get("/")
async def list_stories():
    return {}

@routers.get("/{id}")
async def detail_story():
    return {}

@routers.post("/")
async def create_story():
    return {}

@routers.patch("/{id}")
async def update_story():
    return {}

@routers.delete("/{id}")
async def delete_story():
    return {}            
