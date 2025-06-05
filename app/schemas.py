# app/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    age: int = Field(..., gt=0, le=150)


class UserCreate(UserBase):
    """
    Inherits name, email, and age. Used for POST /users.
    """
    pass


class UserUpdate(BaseModel):
    """
    For PUT /users/{user_id}: all fields optional but validated if provided.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, gt=0, le=150)


class UserRead(UserBase):
    """
    Returned in responses. Includes `id` as a string.
    """
    id: str

    class Config:
        orm_mode = True
