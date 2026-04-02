from fastapi import FastAPI #import fastapi module fastapi is a python class that provides all the functionality for your API.
from enum import Enum
from pydantic import BaseModel #import BaseModel from pydantic module. BaseModel is a class that provides all the functionality for creating data models in FastAPI.

app = FastAPI() #app is an instance of the FastAPI class.

class Careers(str, Enum):
    ceo = "ceo"
    pilot = "pilot"
    engineer = "engineer"


@app.get("/") #this is a path operation decorator that tells FastAPI that the function below is a path operation for the root path ("/") and it will respond to GET requests.
def read_root(): #this is a path operation function
    return {"Hello": "World"}

#PATH PARAMETERS
@app.get("/items/{item_id}") #this is a path operation decorator that tells FastAPI that the function below is a path operation for the path "/items/{item_id}" and it will respond to GET requests. The {item_id} is a path parameter that will be passed to the function as an argument.
def read_item(item_id: int): #this is a path
    return {"item_id": item_id}

@app.get("/careers/{career}")
async def get_career(career: Careers):
    if career is Careers.ceo:
        return {f"Brian is the {career.value} of the company."}
    elif career.value == "pilot":
        return {"Brian is a the captain."}
    elif career.value == "engineer":
        return {"Brian is an engineer."}
    

@app.get("/path/{filepath:path}")
async def read_file(filepath: str):
    return {"filepath": filepath}

#QUERY PARAMETERS

#required parameters
@app.get("/users/")
async def read_users(fname: str, lname:str):
    return {"first name": fname, "last name": lname}

#optional parameters
@app.get("/users/optional")
async def read_users_optional(fname: str | None = None, lname: str | None = None):
    if fname and lname:
        return {"first name": fname, "last name": lname}
    elif fname:
        return {"first name": fname}
    elif lname:
        return {"last name": lname}
    else:
        return {"message": "No parameters provided."}
    
#default parameters
@app.get("/users/default")
async def read_users_default(fname: str = "Brian", lname: str = "Smith"):
    return {"first name": fname, "last name": lname}

#Request Body -> when sending data to the API, we can use a request body to send the data in the body of the request. We can use Pydantic models to define the structure of the request body.
class User(BaseModel):
    name: str
    description: str | None = None
    age: int
    profession: str | None = None

@app.post("/user/")
async def create_user(user: User, car: str | None = None):
    user_age = f"{user.name} is {user.age} years old."
    user_dict = {"sentence": user_age, **user.model_dump()}
    if car:
        user_dict["car"] = car
    return user_dict

@app.put("/user/{user_id}")
async def update_user(user_id: int, user: User, car: str | None = None):
    user_dict = {"user_id": user_id, **user.model_dump()}
    if car:
        user_dict["car"] = car
    return user_dict