from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.book import Book
from app.crud import book as book_crud

router = APIRouter()

@router.get("/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = book_crud.get_books(db, skip=skip, limit=limit)
    return books