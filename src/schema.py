# schema.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class User(BaseModel):
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password : str 