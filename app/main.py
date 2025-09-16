from enum import Enum
from typing import TypedDict, Union

from fastapi import FastAPI

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class ModelResponse(TypedDict):
    model_name: ModelName
    message: str


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(
    item_id: str, q: Union[str, None] = None
) -> dict[str, Union[str, None]]:
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10) -> list[dict[str, str]]:
    return fake_items_db[skip : skip + limit]


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
