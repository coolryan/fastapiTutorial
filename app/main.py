# "main" module, e.g. import app.main
#The main FastAPI
#Import FastAPI
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
#Avoid name collisions
from .internal import admin
#Import the APIRouter
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

#Include the APIRouters for users and items
app.include_router(users.routers)
app.include_router(items.routers)
#Include an APIRouter with a custom prefix, tags, responses, and dependencies
app.include_router(
	admin.router,
	prefix="/admin",
	tags=["admin"],
	dependencies=[Depends(get_token_header)],
	response={418: {"description": "I'm a teapot"}},
)

#Include a path operation
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
