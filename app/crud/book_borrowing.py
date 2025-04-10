# app/crud/book_borrowing.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.book_borrowing import BookBorrowing
from app.schemas.book_borrowing import BookBorrowingCreate, BookBorrowingUpdate

def get_borrowing(db: Session, borrowing_id: int) -> Optional[BookBorrowing]:
    return db.query(BookBorrowing).filter(BookBorrowing.id == borrowing_id).first()

def get_borrowings(db: Session, skip: int = 0, limit: int = 100) -> List[BookBorrowing]:
    return db.query(BookBorrowing).offset(skip).limit(limit).all()

def get_user_borrowings(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[BookBorrowing]:
    return db.query(BookBorrowing).filter(BookBorrowing.user_id == user_id).offset(skip).limit(limit).all()

def get_book_borrowings(db: Session, book_id: int, skip: int = 0, limit: int = 100) -> List[BookBorrowing]:
    return db.query(BookBorrowing).filter(BookBorrowing.book_id == book_id).offset(skip).limit(limit).all()

def get_active_borrowings(db: Session, skip: int = 0, limit: int = 100) -> List[BookBorrowing]:
    return db.query(BookBorrowing).filter(BookBorrowing.is_returned == False).offset(skip).limit(limit).all()

def create_borrowing(db: Session, borrowing: BookBorrowingCreate) -> BookBorrowing:
    db_borrowing = BookBorrowing(
        book_id=borrowing.book_id,
        user_id=borrowing.user_id,
        is_returned=borrowing.is_returned
    )
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing

def update_borrowing(db: Session, borrowing_id: int, borrowing: BookBorrowingUpdate) -> Optional[BookBorrowing]:
    db_borrowing = get_borrowing(db, borrowing_id=borrowing_id)
    if not db_borrowing:
        return None
    
    for key, value in borrowing.dict(exclude_unset=True).items():
        setattr(db_borrowing, key, value)
    
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing

def delete_borrowing(db: Session, borrowing_id: int) -> Optional[BookBorrowing]:
    db_borrowing = get_borrowing(db, borrowing_id=borrowing_id)
    if not db_borrowing:
        return None
    
    db.delete(db_borrowing)
    db.commit()
    return db_borrowing

def return_book(db: Session, borrowing_id: int) -> Optional[BookBorrowing]:
    db_borrowing = get_borrowing(db, borrowing_id=borrowing_id)
    if not db_borrowing:
        return None
    
    if db_borrowing.is_returned:
        return None
    
    db_borrowing.is_returned = True
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing