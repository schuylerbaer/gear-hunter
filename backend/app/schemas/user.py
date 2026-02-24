from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True

# What React sends (requires password)
class UserCreate(UserBase):
    password: str

# What we send back to React (hides password, includes DB generated fields)
class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True # Allows reading from SQLAlchemy models
