import base64

from fastapi import FastAPI, File, Form, UploadFile, status
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class UserBase(BaseModel):
    username: str
    description: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDb(UserBase):
    hashed_password: str

def password_hasher(password: str):
    new_password = "secretpassword" + password
    return new_password

def fake_saver(user: UserIn):
    user_in_db = UserInDb(**user.model_dump(), hashed_password = password_hasher(user.password))
    return user_in_db

@app.post("/user/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: Annotated[UserIn, Form()]):
    user_saved = fake_saver(user)
    return user_saved

@app.post("/upload/profilepicture")
async def upload_profile_pic(file: Annotated[UploadFile, File()]):
    content = await file.read()
    return {
        "name": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "content_base64": base64.b64encode(content).decode("ascii"),
    }
