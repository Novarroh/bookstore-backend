from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    CUSTOMER = "customer"

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_must_be_valid(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None

# This is the User class that's being imported in routes/users.py
class User(UserBase):
    id: int
    role: str
    is_active: bool

    class Config:
        orm_mode = True