from fastapi import APIRouter

routers=APIRouter()


@routers.get("/")
async def list_users():
    return {}

@routers.get("/{id}")
async def detail_user():
    return {}

@routers.post("/")
async def create_user():
    return {}

@routers.patch("/{id}")
async def update_user():
    return {}

@routers.delete("/{id}")
async def delete_user():
    return {}            
