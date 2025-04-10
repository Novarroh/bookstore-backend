# app/models/book.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    quantity = Column(Integer, default=1)  # Total quantity of books
    available_quantity = Column(Integer, default=1)  # Available for borrowing
    
    # Relationship with borrowings
    borrowings = relationship("BookBorrowing", back_populates="book")