# app/models/book_borrowing.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class BookBorrowing(Base):
    __tablename__ = "book_borrowings"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    is_returned = Column(Boolean, default=False)
    
    # Relationships
    book = relationship("Book", back_populates="borrowings")
    user = relationship("User", back_populates="borrowings")