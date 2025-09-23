from enum import Enum
from typing import Any, TypedDict, Union

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class ModelResponse(TypedDict):
    model_name: ModelName
    message: str


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: Union[str, None] = Field(
        default=None,
        title="The description of the item",
        max_length=300,
        examples=["A very nice Item"],
    )
    price: float = Field(examples=[35.4])
    tax: Union[float, None] = Field(default=None, examples=[3.2])


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.post("/items/")
async def create_item(item: Item) -> dict[str, Any]:
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> dict[str, Any]:
    return {"item_id": item_id, **item.model_dump()}


@app.get("/items/{item_id}")
async def read_item(
    item_id: str, q: Union[str, None] = None
) -> dict[str, Union[str, None]]:
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(default=None, max_length=5),
) -> dict[str, Any]:
    results: dict[str, Any] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName) -> ModelResponse:
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str) -> dict[str, str]:
    return {"file_path": file_path}
