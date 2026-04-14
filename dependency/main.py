from fastapi import FastAPI, Depends, Body
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

app = FastAPI()

class User(BaseModel):
    username: str = Field(default="Joe")
    email: EmailStr = Field(default="johndoe@example.com")
    location: str = Field(default = "USA")

#we could create a class dependecy
class CommonParams:
    def __init__(self, username: str, user: User):
        self.username = username
        self.user = user

#we can create a functional dependency
async def common_parameters(username: str, user: Annotated[User, Body()]):
    return user

#declare the line of code as a variable to avoid code repetition
common_dependencies = Annotated[dict, Depends(common_parameters)]

@app.get("/user/{username}")
async def retrieve_user(params: common_dependencies):
    return params

@app.patch("/user/{username}")
async def update_user(params: common_dependencies):
    return params["username"]  