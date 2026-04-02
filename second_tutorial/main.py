#QUERY PARAMETERS WITH VALIDATION
#we use annonated and query

from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import AfterValidator

app = FastAPI()


@app.get("/")
def hello(name: Annotated[str | None, Query(min_length=1, max_length=10)] = "World"):
    return {"message": f"Hello, {name}!"}

#we can also add regex to validate the query parameter
#We use str | None to allow either a string or None value for the name parameter. This means that the name parameter is optional, and if it is not provided, it will default to "World". If a value is provided for the name parameter, it must be a string that matches the specified regex pattern (in this case, it must be "Brian").
@app.get("/hello")
def hello_brian (name: Annotated[str, Query(min_length=1, max_length=5, pattern="^Brian$")]):
    return {"message": f"Hello, {name}!"}


#QUERY PARAMETER LIST
@app.get("/users")
async def users(names: Annotated[list[str] | None, Query()] = None):
    if names:
        return {"names": names}
    
#Default value for a query parameter that is a list
@app.get("/users/default/")
async def users_default(names: Annotated[list[str], Query()] = ["Isaac", "Newton", "Albert", "Einstein"]):
    return {"names": names}

#More metadata -> title, description, alias
#the url will be /users/metadata/?usernames=Isaac&usernames=Newton&usernames=Albert&usernames=Einstein
@app.get("/users/metadata/")
async def users_metadata(names: Annotated[
    list | None,
    Query(
        title="users names",
        description = "A list of user names",
        alias="usernames",
        max_length=5    )
    ] = None):
    if names:
        return {"names": names}
    return {"message": "No names provided"}


#deprecated query parameter -> means that the parameter is obsolete and should not be used
@app.get("/users/deprecated/")
async def users_deprecated(names: Annotated[
    list | None,
    Query(
        title="users names",
        description = "A list of user names",
        alias="usernames",
        max_length=5,
        deprecated=True   #this will mark the parameter as deprecated
    )
] = None):
    if names:
        return {"names": names}
    return {"message": "No names provided"}

#custom validation -> we can use a custom validation function to validate the query parameter

def validate_name(name: str):
    if not name.startswith(("b", "i", "o")):
        return("Name must start with b, i, or o")
    return name

@app.get("/validate/")
async def create_user(name: Annotated[str, AfterValidator(validate_name)]):
    return {"name": name}