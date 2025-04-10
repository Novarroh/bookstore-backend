from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.book_borrowing import BookBorrowing, BookBorrowingCreate, BookBorrowingUpdate, BookBorrowingDetail
from app.crud import book_borrowing as borrowing_crud, book as book_crud, user as user_crud

router = APIRouter()

@router.post("/")
def create_book_borrowing(borrowing: BookBorrowingCreate, db: Session = Depends(get_db)):
    """
    Create a new book borrowing record.
    Only admin and librarian users can create borrowing records.
    """
    # Get the current user from the database
    current_user = user_crud.get_user(db, user_id=borrowing.current_user_id)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Current user not found"
        )
    
    # Check if the user has permission (admin or librarian)
    if current_user.role not in ["admin", "librarian"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and librarian users can create borrowing records"
        )
    # Verify the book exists
    book = book_crud.get_book(db, book_id=borrowing.book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Verify the user exists
    user = user_crud.get_user(db, user_id=borrowing.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if the book is already borrowed and not returned
    active_borrowings = borrowing_crud.get_book_borrowings(db, book_id=borrowing.book_id)
    for active_borrowing in active_borrowings:
        if not active_borrowing.is_returned:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is already borrowed and not yet returned"
            )
    
    borrowing_crud.create_borrowing(db=db, borrowing=borrowing)
    return {"message": "Borrowing record created successfully"}

@router.get("/user/{user_id}", response_model=List[BookBorrowingDetail])
def read_user_borrowings(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve borrowings for a specific user.
    """
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    borrowings = borrowing_crud.get_user_borrowings(db, user_id=user_id, skip=skip, limit=limit)
    return borrowings