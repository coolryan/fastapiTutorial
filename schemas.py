#Create the Pydantic models
##Create initial Pydantic models / schemas
from pydantic import BaseModel

class ItemBase(BaseModel):
	"""docstring for ItemBase"""
	title: str
	description: str | None = None

class ItemCreate(ItemBase):
	"""docstring for ItemCreate"""
	id: int
	owner_id: int

	class Config:
		"""docstring for Config"""
		orm_mode = True

class UserBase(BaseModel):
	"""docstring for UserBase"""
	email: str

class userCreate(UserBase):
	"""docstring for userCreate"""
	password: str

class User(UserBase):
	"""docstring for User"""
	id: int
	is_active: bool
	items: list[Item] = []

	class config:
		"""docstring for config"""
		orm_mode = True
