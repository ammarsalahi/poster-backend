from fastapi import APIRouter

routers=APIRouter()

routers.post("/signin")
async def Signin():
    return {}

routers.post("/signup")
async def Signup():
    return {}

routers.post("/signout")
async def Signout():
    return {}


routers.post("/change_passowrd")
async def ChangePassowrd():
    return {}

routers.post("/email_valid")
async def EmailValid():
    return {}    

routers.post("/verify")
async def Verify():
    return {}    