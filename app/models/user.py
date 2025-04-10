from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    CUSTOMER = "customer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)  # Note: In a real app, you should hash passwords
    role = Column(String, default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)
    
    # Relationship with books
    borrowings = relationship("BookBorrowing", back_populates="user")