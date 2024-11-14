from fastapi import FastAPI
from routers import *

app = FastAPI(
    title="Poster API",
    docs_url="/",
    description="Created by Ammar Salahi (just for fun!)"
)

app.add_route("/users",userRouters)
app.add_route("/comments",commentRouters)
app.add_route("/posts",postRouters)
app.add_route("/stories",storyRouters)
app.add_route("/settings",settingRouters)

