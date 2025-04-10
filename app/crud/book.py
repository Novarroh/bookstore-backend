from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    return db.query(Book).offset(skip).limit(limit).all()

def get_user_books(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Book]:
    return db.query(Book).filter(Book.borrower_id == user_id).offset(skip).limit(limit).all()

def create_book(db: Session, book: BookCreate, borrower_id: int) -> Book:
    db_book = Book(
        title=book.title,
        author=book.author,
        borrower_id=borrower_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[Book]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> Optional[Book]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    db.delete(db_book)
    db.commit()
    return db_book