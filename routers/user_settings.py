from fastapi import APIRouter

routers=APIRouter()


@routers.get("/")
async def list_settings():
    return {}

@routers.get("/{id}")
async def detail_setting():
    return {}

@routers.post("/")
async def create_setting():
    return {}

@routers.patch("/{id}")
async def update_setting():
    return {}

@routers.delete("/{id}")
async def delete_setting():
    return {}            
