from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

#users
class RegisterInput(BaseModel):
    username : str = Field(min_length=3, max_length=40, pattern=r"^[a-zA-Z0-9_]+$")
    password : str = Field(min_length=8)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    username : str
    role : str
    is_active : bool


class TokenOut(BaseModel):
    access_token: str
    token_type : str = "bearer"

#posts
class PostCreate(BaseModel):
    title : str = Field(min_length=3, max_length=200)
    content : str = Field(min_length=1)

class PostUpdate(BaseModel):
    title : str | None = Field(default = None, min_length=3, max_length=200)
    content : str | None = Field(default = None, min_length=1)

class PostOut(BaseModel): #это ответ сервера
    model_config = ConfigDict(from_attributes=True)
    id : int
    title : str
    content : str
    is_hidden : bool
    author_id : int
    created_at : datetime