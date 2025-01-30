from fastapi import APIRouter
from app.api.routes import *
from app.api.graphqls import Mutation,Query
from .deps import sessionDep,userDep
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.file_uploads import Upload
from starlette.datastructures import UploadFile



app_router = APIRouter()

app_router.include_router(authRouters,prefix="/auth",tags=['auth'])
app_router.include_router(userRouters,prefix="/users",tags=['users'])
app_router.include_router(postRouters,prefix="/posts",tags=['posts'])
app_router.include_router(commentRouters,prefix="/comments",tags=['comments'])
app_router.include_router(storyRouters,prefix="/stories",tags=['stories'])
app_router.include_router(settingRouters,prefix="/settings",tags=['settings'])
app_router.include_router(mediaRouters,prefix="/medias",tags=['medias'])
app_router.include_router(followRouters,prefix="/follows",tags=['follows'])
app_router.include_router(notifyRoouters,prefix="/notifies",tags=['notifies'])
app_router.include_router(messageRouters,prefix="/messages",tags=['messages'])
app_router.include_router(validationRouters,prefix="/validations",tags=['validations'])


# define graphQL router

async def get_context(db:sessionDep,user:userDep):
    return {
        "session":db,
        "current_user":user
    }
    
schema=strawberry.Schema(query=Query,mutation=Mutation)
graphql_router = GraphQLRouter(schema,context_getter=get_context)


app_router.include_router(graphql_router,prefix="/graphql")
