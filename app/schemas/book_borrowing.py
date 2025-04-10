# app/schemas/book_borrowing.py
from typing import Optional
from pydantic import BaseModel
from app.schemas.book import Book
from app.schemas.user import User

class BookBorrowingBase(BaseModel):
    book_id: int
    user_id: int
    is_returned: bool = False

class BookBorrowingCreate(BookBorrowingBase):
    current_user_id: int

class BookBorrowingUpdate(BaseModel):
    is_returned: Optional[bool] = None

class BookBorrowing(BookBorrowingBase):
    id: int

    class Config:
        orm_mode = True

class BookBorrowingDetail(BookBorrowing):
    book: Optional[Book] = None
    user: Optional[User] = None