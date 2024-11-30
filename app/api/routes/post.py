from fastapi import APIRouter

routers=APIRouter()


@routers.get("/")
async def list_posts():
    return {}

@routers.get("/{id}")
async def detail_post():
    return {}

@routers.post("/")
async def create_post():
    return {}

@routers.patch("/{id}")
async def update_post():
    return {}

@routers.delete("/{id}")
async def delete_post():
    return {}            
