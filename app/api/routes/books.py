from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.book import Book
from app.crud import book as book_crud

router = APIRouter()

@router.get("/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of books with pagination support.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Number of records to return. Defaults to 100.
        db (Session, optional): Database session dependency.

    Returns:
        List[Book]: List of books.
    """

    books = book_crud.get_books(db, skip=skip, limit=limit)
    return books