from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4

app = FastAPI()


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class Education(BaseModel):
    school: str = Field(description="The name of the school")
    program: str = Field(description="The program of the user")
    gpa: float = Field(gt=0.0, le=5.0, description="The GPA of the user")

class User(BaseModel):
    user_id: UUID = Field(default_factory=uuid4, description="The ID of the user")
    first_name: str = Field(default="Brian", description="The first name of the user")
    last_name: str | None = Field(default=None, description="The last name of the user")
    age: int = Field(gt=0, description="The age of the user")
    email: EmailStr = Field(description="The email of the user")
    gender: Gender = Field(default=Gender.male, description="The gender of the user")
    hobbies: set[str] = Field(default=set(), description="Hobbies of the user")
    education: Education = Field(description="The education of the user")

@app.get("/")
def read_user(user: User):
    return user

@app.post("/user")
async def create_user(user: User):
    return user.model_dump()

@app.get("/education/multiple")
async def read_multiple_education(education: list[Education]):
    return education