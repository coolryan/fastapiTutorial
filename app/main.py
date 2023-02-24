# "main" module, e.g. import app.main
#The main FastAPI
#Import FastAPI
from fastapi import Depends, FastAPI, APIRouter, Header, HTTPException

from pydantic import BaseModel

from .dependencies import get_query_token, get_token_header
#Avoid name collisions
from .internal import admin
#Import the APIRouter
from .routers import items, users

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

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

router = APIRouter()

@router.post("/")
async def update_admin():
	return {"message": "admin getting schwify"}

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item
