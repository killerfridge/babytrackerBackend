from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta


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
    is_awake: bool
    is_feeding: bool


class Feed(BaseModel):
    id: int
    feed_start: datetime
    feed_end: Optional[datetime]
    feed_length: Optional[timedelta]

    class Config:
        orm_mode = True


class Sleep(BaseModel):
    id: int
    sleep_start: datetime
    sleep_end: Optional[datetime]
    sleep_length: Optional[timedelta]

    class Config:
        orm_mode = True


class WeightBase(BaseModel):
    value: float
    baby_id: float


class TempBase(BaseModel):
    value: float
    baby_id: float


class BabyAll(BaseModel):
    Baby: Baby
    SleepSession: Optional[Sleep]
    FeedSession: Optional[Feed]


