from decimal import Decimal
from unicodedata import decimal
from graphene import Int
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

#this model is used for the pydantic model to check the data.  see post: Post
class PostBase(BaseModel):
    temp: int
    press: int
    humid: int
    wind_speed: int
    wind_direction: int
    bno_direction: int
    event_direction: int
    current: int
    voltage: float
    power: int
#    date: datetime

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    # owner_id: int
    # owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None