from fastapi import APIRouter

routers=APIRouter()


@routers.get("/")
async def list_comments():
    return {}

@routers.get("/{id}")
async def detail_comment():
    return {}

@routers.post("/")
async def create_comment():
    return {}

@routers.patch("/{id}")
async def update_user():
    return {}

@routers.delete("/{id}")
async def delete_user():
    return {}            
