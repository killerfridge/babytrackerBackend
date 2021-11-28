from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: datetime


class UserCreate(UserBase):
    password: str


class BabyBase(BaseModel):

    class Config:
        orm_mode = True


class BabyCreate(BabyBase):
    name: Optional[str]


class Baby(BabyBase):
    id: int
    name: Optional[str]
    user_id: int
