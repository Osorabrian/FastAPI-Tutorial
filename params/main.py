from fastapi import Body, Cookie, FastAPI, Header
from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime

app = FastAPI()

class Cookies(BaseModel):
    session_id: int
    facebook_tracker: str | None
    google_tracker: str | None
    model_config = {"extra": "forbid"}

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    traceparent: str | None
    x_tags: list[str]

class Item(BaseModel):
    item_id: UUID = Field(default_factory=uuid4)
    name: str
    price: Decimal | None = Field(default = None, decimal_places=2)
    date: datetime = Field(default_factory=datetime.now)

#we can define the cookie and header paremeters in our path operation function
#we use snake_case when defining a header, shixh will get converted to have a hyphen between words
@app.get("/items/")
async def read_items(
    async_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None #will get converted to user-agent to avoud thois we add convert_underscores=Fasle in header 
    ):
    return {"async_id": async_id}

#duplicate headers, same header with multiple values
@app.get("/item/{item_id}")
async def retrieve_item(
    item_id: int,
    x_token: Annotated[list[str] | None, Header()] = None
):
    return {"X-Token": x_token}

@app.post("/item/", response_model=Item)
async def create_item(
    item: Annotated[Item, Body()],
    cookies: Annotated[Cookies, Cookie()],
    headers: Annotated[CommonHeaders, Header()]
):
    return item