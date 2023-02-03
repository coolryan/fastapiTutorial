from enum import Enum

from fastapi import FastAPI, Path, Query

from pydantic import BaseModel

class ModelName(str, Enum):
	"""docstring for ModelName"""
	alexnet = "alexnet"
	resnet = "resnet"
	lenet = "lenet"

class Item(BaseModel):
	"""docstring for Item"""
	name: str
	description: str | None = None
	price: float
	tax: float | None = None

class User(BaseModel):
	"""docstring for User"""
	username: str
	fullname: str | None = None

app = FastAPI()

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
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
	results = {"item_id": item_id, "item": item, "user": user}
	return results

##Singular values in body
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body()):
	results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
	return results
