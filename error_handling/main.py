from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from uuid import UUID, uuid4
from decimal import Decimal

app = FastAPI()

class Tags(str, Enum):
    user = "user"
    items = "items"

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class User(BaseModel):
    username: str
    email: EmailStr | None
    gender: str = Field(default=Gender.male)
    location: str
    model_config = {"extra": "forbid"}

class Item(BaseModel):
    item_id: UUID = Field(default_factory=uuid4)
    name: str
    price: Decimal = Field(ge=0.0, decimal_places=2)
    quantity: int
    
@app.post("/user/", status_code=status.HTTP_201_CREATED, tags=[Tags.user], response_model=Item)
async def create_user(user: User):
    return user

@app.post("/item/", status_code=status.HTTP_201_CREATED, tags=[Tags.items], response_description="creates an item and calculates total value")
async def create_item(item: Item):
    total_value = item.price * item.quantity
    result = {**item.model_dump(), "total_value":total_value}
    return result