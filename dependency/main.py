from fastapi import FastAPI, Depends, Body, Cookie
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
#async def common_parameters(username: str, user: Annotated[User, Body()]):
#    return user

#declare the line of code as a variable to avoid code repetition
#common_dependencies = Annotated[dict, Depends(common_parameters)]

#This is a subdependency
def query_extractor(q: str | None = None):
    return q

#This is  a dependency that depends on the subdependency
def query_or_cookie_extractor(q: Annotated[str, Depends(query_extractor)], last_query: Annotated[str | None, Cookie()] = None):
    if q:
        return {"q": q}
    else:
        return {"last_query": last_query}

#we use the dependency that calls a subdependency
@app.get("/user/{username}")
async def retrieve_user(username: str, query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]):
    return username

#utilizing the calss parameter
@app.put("/user/{username}")
async def put_user(params: Annotated[CommonParams, Depends()]):
    return params.username

@app.patch("/user/{username}")
async def update_user(params: Annotated[CommonParams, Depends()]):
    return params.username