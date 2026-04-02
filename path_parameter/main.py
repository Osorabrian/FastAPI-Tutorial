from fastapi import FastAPI, Path, Query, Body
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    user_id: int
    fname: str
    lname: str
    age: int
    gender: str

class Grades(BaseModel):
    maths: int = Field(..., gt=0, le=100)
    science: int = Field(..., gt=0, le=100)
    english: int = Field(..., gt=0, le=100) 

@app.get("/user/{user_id}")
async def read_user(
    user_id: Annotated[int, Path(title="The ID of the user", gt=0, le=10)],
    fname: Annotated[str | None, Query()] = None,
    lname: Annotated[str | None, Query()] = None,
    ):
    result = {"user_id": user_id}
    if fname:
        result["fname"] = fname
    if lname:
        result["lname"] = lname
    return result

@app.post("/user/")
async def create_user(user: User):
    return {"user", user}

@app.put("/user/{user_id}/grades")
async def update_user_grades(user_id: int, user:Annotated[User, Body()], grades: Annotated[Grades, Body(embed=True)]):
    return {"user_id": user_id, "grades": grades}