from enum import Enum
from fastapi import Body, FastAPI
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from typing import Annotated

app = FastAPI()


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

#create a submodel
class Education(BaseModel):
    school: str = Field(description="The name of the school")
    program: str = Field(description="The program of the user")
    gpa: float = Field(gt=0.0, le=5.0, description="The GPA of the user")

#we include the submodel in the main model
#we have included the field in the main model
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

#we can specify the example of return value
@app.post("/user")
async def create_user(user: Annotated[User, Body(examples=[
    {
        "first_name" : "Brian",
        "last_name": "Isaboke",
        "age": 20,
        "email": "brian@example.com",
        "gender": "male",
        "hobbies": ["reading", "coding", "traveling"],
        "education": {
            "school": "Harvard University",
            "program": "Computer Science",
            "gpa": 3.9,
        }
    }
])]):
    return user.model_dump()

#we can specify how we want to return the data
#we can specify the open_api exmaple of data we expecting to be returned
@app.post("/education/multiple")
async def read_multiple_education(
    education: Annotated[
        list[Education],
        Body(
            openapi_examples={
                "normal example": {
                    "summary": "A normal example",
                    "value": [
                        {
                            "school": "Harvard University",
                            "program": "Computer Science",
                            "gpa": 3.9,
                        }
                    ]
                },
                "converted example": {
                    "summary": "A converted example",
                    "value": [
                        {
                            "school": "Stanford University",
                            "program": "Data Science",
                            "gpa": "3.8",
                        }
                    ]
                }
            }
        ),
    ]
):
    return education