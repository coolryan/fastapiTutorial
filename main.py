from typing import Union

from typing import Any

from enum import Enum

from datetime import datetime, time, timedelta

from uuid import UUID

from fastapi import Body, Cookie, FastAPI, Path, Query, Header, status, Form

from pydantic import BaseModel, Field, HttpUrl, EmailStr

class UserBase(BaseModel):
	"""docstring for UserBase"""
	username: str
	email: EmailStr
	full_name: str | None = None

# class UserIn(BaseModel):
# 	"""docstring for UserIn"""
# 	username: str
# 	password: str
# 	email: EmailStr
# 	full_name: str | None = None

class UserIn(UserBase):
	"""docstring for UserIn"""
	password: str

# class UserOut(BaseModel):
# 	"""docstring for UserOut"""
# 	username: str
# 	email: EmailStr
# 	full_name: str | None = None

class UserOut(UserBase):
	"""docstring for UserOut"""
	pass

# class UserInDB(BaseModel):
# 	"""docstring for UserInDB"""
# 	username: str
# 	hashed_password: str
# 	email: EmailStr
# 	full_name: str | None = None

class UserInDB(UserBase):
	"""docstring for UserInDB"""
	hashed_password: str

class Image(BaseModel):
	"""docstring for Image"""
	url: HttpUrl
	name: str

class ModelName(str, Enum):
	"""docstring for ModelName"""
	alexnet = "alexnet"
	resnet = "resnet"
	lenet = "lenet"

class Item(BaseModel):
	"""docstring for Item"""
	name: str
	description: str | None = Field(
		default=None, title="The description of the item", max_length=300
	)
	price: float = Field(gt=0, description="The price must be greater than zero")
	tax: float | None = None
	tags: list[str] = []
	image: Image | None = None

class Config:
	"""docstring for Config"""
	schema_extra = {
		"example": {
			"name": "Foo",
			"description": "A very nice Item",
			"price": 35.4,
			"tax": 3.2,
		}
	}
		
class Offer(BaseModel):
	"""docstring for Offer"""
	name: str
	description: str | None = None
	price: float
	items: list[Item]
		
class User(BaseModel):
	"""docstring for User"""
	username: str
	full_name: str | None = None

app = FastAPI()

class BaseItem(BaseModel):
	"""docstring for BaseItem"""
	description: str
	type: str

class CarItem(BaseItem):
	"""docstring for CarItem"""
	type = "car"

class PlaneItem(BaseItem):
	"""docstring for PlaneItem"""
	type = "plane"
	size: int

# class Item2(BaseModel):
# 	"""docstring for Item2"""
# 	name: str
# 	description: str

fake_item_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items/{item_id}")
# async def read_item(item_id: float):
# 	return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
	return {"user_id" : "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
	return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
	if model_name is ModelName.alexnet:
		return {"model_name": model_name, "message": "Deep Learning FTW!"}

	if model_name.value == "lenet":
		return {"model_name": model_name, "message": "LeCNN all the images"}

	return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
	return {"file_path": file_path}
	
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
	return fake_item_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
	item = {"item_id": item_id}
	if q:
		item.update({"q": q})
	if not short:
		item.update(
			{"description": "This is an amazing item that has a long description"}
		)
	return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
	user_id: int, item_id: str, q: str | None = None, short: bool = False
):
	item = {"item_id": item_id, "owner_id": user_id}
	if q:
		item.update({"q": q})
	if not short:
		item.update(
			{"description": "This is an amazing item that has a long description"}
		)
	return item

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
	item = {"item_id": item_id, "needy": needy}
	return item

@app.get("/items/{item_id}")
async def read_user_item(
	item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
	item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
	return item

@app.post("/items/")
async def create_item(item: Item):
	item_dict = item.dict()
	if item.tax:
		price_with_tax = item.price + item.tax
		item_dict.update({"price_with_tax": price_with_tax})
	return item_dict

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
	return {"item_id": item_id, **item.dict()}

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
	result = {"item_id": item_id, **item.dict()}
	if q:
		result.update({"q": q})
	return result

#Path Parameters and Numeric Validations

# @app.get("/items/{item_id}")
# async def read_items(
# 	item_id: int = Path(title="The ID of the item to get"),
# 	q: str | None = Query(default=None, alias="item-query"),
# ):
# 	results = {"item_id": item_id}
# 	if q:
# 		results.update({"q": q})
# 	return results

@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
	results = {"item_id": item_id}
	if q:
		results.update({"q": q})
	return results

@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
	results = {"item_id": item_id}
	if q:
		results.update({"q": q})
	return results

##Number validations: greater than or equal
@app.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):
	results = {"item_id": item_id}
	if q:
		results.update({"q": q})
	return results

##Number validations: greater than and less than or equal
@app.get("/items/{item_id}")
async def read_items(
	*,
	item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
	q: str,
):
	results = {"item_id": item_id}
	if q:
		results.update({"q": q})
	return results

##Number validations: floats, greater than and less than
@app.get("/items/{item_id}")
async def read_items(
	*,
	item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
	q: str,
	size: float = Query(gt=0, lt=10.5)
):
	results = {"item_id": item_id}
	if q:
		results.update({"q": q})
	return results

#Body - Multiple Parameters

##Mix Path, Query and body parameters
@app.put("/items/{item_id}")
async def update_item(
	*,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str | None = None,
    item: Item | None = None,
):
	results = {"item_id": item_id}
	if q:
		results.update({"q": q})
	if item:
		results.update({"item": item})
	return results

##Multiple body parameters
@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
	results = {"item_id": item_id, "item": item, "user": user}
	return results

#Singular values in body
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, user: User, importance: int = Body()):
# 	results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
# 	return results

#Multiple body params and query
# @app.put("/items/{item_id}")
# async def update_item(
# 	*,
#     item_id: int,
#     item: Item,
#     user: User,
#     importance: int = Body(gt=0),
#     q: str | None = None
# ):
# 	results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
# 	if q:
# 		results.update({"q": q})
# 	return results

#Embed a single body parameter
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(embed=True)):
# 	results = {"item_id": item_id, "item": item}
# 	return results

#Body - Fields
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(embed=True)):
# 	results = {"item_id": item_id, "item": item}
# 	return results

#Deeply nested models
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

#Bodies of pure lists
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
	return images

#Bodies of arbitrary dicts
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
	return weights

#Declare Request Example Data
##Pydantic schema_extra
@app.put("/items3/{item_id}")
async def update_item(
	item_id: int,
	item: Item = Body(
		example={
			"name": "Foo",
			"description": "A very nice Item",
			"price": 35.4,
			"tax": 3.2,
		},
	),
):
	results = {"item_id": item_id, "item": item}
	return results

#Body with multiple examples
@app.put("/items3/{item_id}")
async def update_item(
	*,
	item_id: int,
	item: Item = Body(
		examples={
			"normal": {
				"summary": "A normal example",
				"description": "A **normal** item works correctly.",
				"value": {
					"name": "Foo",
					"description": "A very nice Item",
					"price": 35.4,
					"tax": 3.2,
				},
			},
			"converted": {
				"summary": "An example with converted data",
				"description": "FastAPI can convert price `strings` to actual `numbers` automatically",
				"value": {
					"name": "Bar",
					"price": "35.4",
				},
			},
			"invalid": {
				"summary": "Invalid data is rejected with an error",
				"value": {
					"name": "Baz",
					"price": "thirty five point four",
				},
			},
		},
	),
):
	results = {"item_id": item_id, "item": item}
	return results

#Extra Data Types
@app.put("/items4/{item_id}")
async def read_items(
	item_id: UUID,
	start_datetime: datetime | None = Body(default=None),
	end_datetime: datetime | None = Body(default=None),
	repeat_at: time | None = Body(default=None),
    process_after: timedelta | None = Body(default=None),
):
	start_process = start_datetime + process_after
	duration = end_datetime - start_process
	return {
		"item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
	}

#Cookie Parameters
@app.get("/items_cookies/")
async def read_items(ads_id: str | None = Cookie(default=None)):
	return {"ads_id": ads_id}

#Header Parameters
@app.get("/items2/")
async def read_items(user_agent: str | None = Header(default=None)):
	return {"User-Agent": user_agent}

#Duplicate headers
@app.get("/items_xtoken/")
async def read_items(x_token: list[str] | None = Header(default=None)):
	return {"X-Token values": x_token}

#Response Model - Return Type
@app.post("/items_responseModel/")
async def item_resposne(item: Item) -> Item:
	return item

#esponse_model Parameter
@app.post("/items_responseModel2/", response_model=list[Item])
async def tem_resposne2() -> Any:
	return [
		{"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0}
	]

#response_model Priority & Add an output model
@app.post("/user2/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
	return user

#Return Type and Data Filtering
# @app.post("/user3/")
# async def create_user3(user: UserIn) -> BaseUser:
# 	return user

#Extra Models
##Multiple models
def fake_password_hasher(raw_password: str):
	return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
	hashed_password = fake_password_hasher(user_in.password)
	user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
	print("User saved! .. not really")
	return user_in_db

@app.post("/user4/", response_model=UserOut)
async def create_user4(user_in: UserIn):
	user_saved = fake_save_user(user_in)
	return user_saved

#Union or anyOf
items = {
	"item1": {"description": "All my friends drive a low rider", "type": "car"},
	"item2": {
		"description": "Music is my aeroplane, it's my aeroplane",
		"type": "plane",
		"size": 5,
	},
}

@app.get("/item5/{item_id}", response_model=Union[PlaneItem, CarItem])
async def vehicle_description(item_id: str):
	return items[item_id]

# #List of models
# items2 = [
#     {"name": "Foo", "description": "There comes my hero"},
#     {"name": "Red", "description": "It's my aeroplane"},
# ]

# #Response with arbitrary dict
# @app.get("/keyword-weights/", response_model=dict[str, float])
# async def read_keyword_weights():
# 	return items2

#Response Status Code
@app.post("/items2/", status_code=201)
async def create_item2(name: str):
	return {"name": name}

@app.post("/items3/", status_code=status.HTTP_201_CREATED)
async def create_item3(name: str):
	return {"name": name}

#Import Form
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
	return {"username": username}
