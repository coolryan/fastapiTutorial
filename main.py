from typing import Any, Union

from enum import Enum

from datetime import datetime, time, timedelta

from uuid import UUID

from fastapi import Body, Cookie, Depends, FastAPI, Path, Query, Header, status, Form, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from starlette.exceptions import HTTPException as StarletteHTTPException

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

fake_db = {}

# class Item(BaseModel):
# 	"""docstring for Item"""
# 	name: str
# 	description: str | None = Field(
# 		default=None, title="The description of the item", max_length=300
# 	)
# 	price: float = Field(gt=0, description="The price must be greater than zero")
# 	tax: float | None = None
# 	tags: list[str] = []
# 	image: Image | None = None

class Item(BaseModel):
	"""docstring for Item"""
	title: str
	timestamp: datetime
	description: str | None = None

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

class UnicornException(Exception):
	"""docstring for UnicornException"""
	def __init__(self, name: str):
		self.name = name

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

class Tags(Enum):
	"""docstring for Tags"""
	items = "items"
	users = "users"

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

#Request Files
@app.post("/files/")
async def create_file(file: bytes = File()):
	return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
	return {"filename": file.filename}

#UploadFile with Additional Metadata
@app.post("/files2/")
async def create_file2(file: bytes = File(description="A file read as bytes")):
	return {"file_size": len(file)}

@app.post("/uploadfile2/")
async def create_upload_file2(
    file: UploadFile = File(description="A file read as UploadFile"),
):
	return {"filename": file.filename}

#Multiple File Uploads
@app.post("/files3/")
async def create_files3(files: list[bytes] = File()):
	return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles3/")
async def create_upload_files3(files: list[UploadFile]):
	return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
	content = """ 
		<body>
			<form action="/files3/" enctype="multipart/form-data" method="post">
				<input name="files" type="file" multiple>
				<input type="submit">
			</form>
			<form action="/uploadfiles3/" enctype="multipart/form-data" method="post">
				<input name="files" type="file" multiple>
				<input type="submit">
			</form>
		</body>
	"""
	return HTMLResponse(content=content)

#Request Forms and Files
@app.post("/files4/")
async def create_file4(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

#Use HTTPException
items2 = {"foo": "The Foo Wrestlers"}
@app.get("/items6/{item_id}")
async def read_item6(item_id: str):
	if item_id not in items2:
		raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "There goes my error"},)
	return {"item": items2[item_id]}

#Install custom exception handlers
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

#Re-use FastAPI's exception handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.get("/items7/{item_id}")
async def read_item_execptions(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

#Use the RequestValidationError body
@app.get("/items/", tags=[Tags.items])
async def get_items():
	return ["Portal gun", "Plumbus"]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]

#Summary and description
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item

#Description from docstring
@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
	""" 
	Create an item with all the information:

	- **name**: each item must have a name
	- **description**: a long description
	- **price**: required
	- **tax**: if the item doesn't have tax, you can omit this
	- **tags**: a set of unique tag strings for this item
	"""
	return item

#Response description
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
	""" 
	Create an item with all the information:

	- **name**: each item must have a name
	- **description**: a long description
	- **price**: required
	- **tax**: if the item doesn't have tax, you can omit this
	- **tags**: a set of unique tag strings for this item
	"""
	return item

#JSON Compatible Encoder
##Using the jsonable_encoder
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data

#Body - Updates
##Update replacing with PUT
class Item3(BaseModel):
	"""docstring for Item3"""
	name: str | None = None
	description: str | None = None
	price: float | None = None
	tax: float = 10.5
	tags: list[str] = []
	
items3 = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items8/{item_id}", response_model=Item3)
async def read_item(item_id: str):
    return items3[item_id]

@app.put("/items8/{item_id}", response_model=Item3)
async def update_item(item_id: str, item: Item3):
    update_item_encoded = jsonable_encoder(items3)
    items3[item_id] = update_item_encoded
    return update_item_encoded

@app.patch("/items9/{item_id}", response_model=Item3)
async def update_item(item_id: str, item: Item3):
    stored_item_data = items3[item_id]
    stored_item_model = Item3(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items3[item_id] = jsonable_encoder(updated_item)
    return updated_item

#Dependencies - First Steps
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items10/")
async def read_items3(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users2/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

#Classes as Dependencies
##Classes as dependencies
class Cat:
	"""docstring for Cat"""
	def __init__(self, name: str):
		self.name = name

fluffy = Cat(name="Mr Fluffy")

fake_items_db2 = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
	"""docstring for CommonQueryParams"""
	def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
		self.q = q
		self.skip = skip
		self.limit = limit

@app.get("/items11/")
async def read_Common_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db2[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

#Shortcut
@app.get("/items12/")
async def read_Common_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db2[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

#Sub-dependencies
def query_extractor(q: str | None = None):
	return q

def query_or_cookie_extractor(
	q: str = Depends(query_extractor), last_query: str | None = Cookie(default=None)
):
	if not q:
		return last_query
	return q

@app.get("/items13/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}

#Using the same dependency multiple times
# async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
# 	return {"fresh_value": fresh_value}

#Dependencies in path operation decorators
##Add dependencies to the path operation decorator
async def verify_token(x_token: str = Header()):
	if x_token != "fake-super-secret-token":
		raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header()):
	if x_key != "fake-super-secret-key":
		raise HTTPException(status_code=400, detail="X-Key header invalid")
	return x_key

@app.get("/items15/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_token_key_items():
	return [{"item": "Foo"}, {"item": "Bar"}]

#Global Dependencies
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

@app.get("/items16/")
async def read_items_depends():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]

@app.get("/users5/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

#Dependencies with yield
##A database dependency with yield
async def get_db():
	db = DBSession()
	try:
		yield db
	finally:
		db.close()
#Sub-dependencies with yield
async def dependency_a():
	dep_a = generate_dep_a()
	try:
		yield dep_a
	finally:
		dep_a.close()

async def dependency_b(dep_a=Depends(dependency_a)):
	dep_b = generate_dep_b()
	try:
		yield dep_b
	finally:
		dep_b.close(dep_a)

async def dependency_c(dep_b=Depends(dependency_b)):
	dep_c = generate_dep_c()
	try:
		yield dep_c
	finally:
		dep_c.close(dep_b)

#Dependencies with yield and HTTPException
#Context Managers
# with open("./fake_fastapi.txt") as f:
# 	contents = f.read()
# 	print(contents)

#Using context managers in dependencies with yield
class MySuperContextManager:
	"""docstring for MySuperContextManager"""
	def __init__(self):
		self.db = DBSession()

	def __enter__(self):
		return self.db

	def __exit__(self, exc_type, exc_value, traceback):
		self.db.close()

async def get_db():
	with MySuperContextManager() as db:
		yield db

fake_users_db = {
	"johndoe": {
		"username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
	},
	"alice": {
		"username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
	},
}

#Security - First Steps
app2 = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app2.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

#Create a user model
class User(BaseModel):
	"""docstring for User"""
	username: str
	email: str | None = None
	full_name: str | None = None
	disabled: bool | None = None

class UserInDB(User):
	"""docstring for UserInDB"""
	hashed_password: str

#Create a get_current_user dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
	user = fake_decode_token(token)
	if not user:
		raise HTTPException(
		    status_code=status.HTTP_401_UNAUTHORIZED,
		    detail="Invalid authentication credentials",
		    headers={"WWW-Authenticate": "Bearer"},
		)
	return user

#Inject the current user

#Simple OAuth2 with Password and Bearer
def fake_hash_password(password: str):
    return "fakehashed" + passworddef 

def get_user(db, username: str):
	if username in db:
		user_dict = db[username]
		return UserInDB(**user_dict)

def fake_decode_token(token):
	# This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app2.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app2.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
	return current_user
