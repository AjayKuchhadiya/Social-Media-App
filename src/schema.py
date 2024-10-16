# schema.py -> here we define how the data should come and go , in what structure and rules it should follow 
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    user_id : int
    created_at : datetime
    user : User   # sqlalchemy relationship 
    
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password : str 

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str]