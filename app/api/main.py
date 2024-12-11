from fastapi import APIRouter
from api.routes import *
from api.graphqls import Mutation,Query
from .deps import sessionDep
import strawberry
from strawberry.fastapi import GraphQLRouter
app_router = APIRouter()

app_router.include_router(authRouters,prefix="/auth",tags=['auth'])
app_router.include_router(userRouters,prefix="/users",tags=['users'])
app_router.include_router(postRouters,prefix="/posts",tags=['posts'])
app_router.include_router(commentRouters,prefix="/comments",tags=['comments'])
app_router.include_router(storyRouters,prefix="/stories",tags=['stories'])
app_router.include_router(settingRouters,prefix="/settings",tags=['settings'])
app_router.include_router(mediaRouters,prefix="/medias",tags=['medias'])

#define graphQL router
# schema=strawberry.Schema(mutation=Mutation,query=Query)
# graphql_router = GraphQLRouter(schema)

# app_router.include_router(graphql_router,prefix="/graphql")
