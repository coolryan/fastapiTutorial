# "users" submodule, e.g. import app.routers.users
#Import APIRouter
from fastapi import APIRouter

router = APIRouter()

#Path operations with APIRouter
@router.get("/users/", tags=["users"])
async def read_users():
	return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
	return {"username": "fakecurrentuser"}

@router.get("/user/{username}", tags=["users"])
async def read_user(username: str):
	return {"username": username}
