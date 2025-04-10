from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None

class Book(BookBase):
    id: int
    quantity: int
    available_quantity: int

    class Config:
        orm_mode = True