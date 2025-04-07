from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field()
    email: EmailStr = Field()


class UserCreate(UserBase):
    password: Optional[str] = ""


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    user_id: int = Field()
    created_at: datetime = Field()
