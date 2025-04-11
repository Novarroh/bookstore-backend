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
    Create a new borrowing record
    
    Args:
        borrowing (BookBorrowingCreate): The borrowing record to be created
        db (Session, optional): The database session dependency. Defaults to Depends(get_db).
    
    Raises:
        HTTPException: 404 Not Found if the current user is not found
        HTTPException: 403 Forbidden if the current user is not an admin or librarian
        HTTPException: 404 Not Found if the book is not found
        HTTPException: 400 Bad Request if the book is not available for borrowing (quantity is 0)
        HTTPException: 404 Not Found if the user is not found
        HTTPException: 400 Bad Request if the book is already borrowed and not yet returned
    
    Returns:
        dict: A message indicating the successful creation of the borrowing record
    """
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
    
    # Check if book is available (quantity > 0)
    if book.available_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not available for borrowing (quantity is 0)"
        )
    
    
    # Verify the user exists
    user = user_crud.get_user(db, user_id=borrowing.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if the book is already borrowed and not returned
    active_borrowings = borrowing_crud.get_user_book_borrowings(db, book_id=borrowing.book_id, user_id=borrowing.user_id)
    for active_borrowing in active_borrowings:
        if not active_borrowing.is_returned:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is already borrowed and not yet returned"
            )
    
    borrowing_crud.create_borrowing(db=db, borrowing=borrowing)

    # Reduce the book quantity
    book.available_quantity = book.available_quantity - 1
    db.add(book)
    db.commit()
    db.refresh(book)

    return {"message": "Borrowing record created successfully"}

@router.get("/user/{user_id}", response_model=List[BookBorrowingDetail])
def read_user_borrowings(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all borrowing records for a given user

    Args:
        user_id (int): User id
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Number of records to return. Defaults to 100.

    Raises:
        HTTPException: 404 Not Found if the user is not found

    Returns:
        List[BookBorrowingDetail]: List of borrowing records
    """
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    borrowings = borrowing_crud.get_user_borrowings(db, user_id=user_id, skip=skip, limit=limit)
    return borrowings

@router.put("/{borrowing_id}/return")
def return_borrowed_book(borrowing_id: int, db: Session = Depends(get_db)):
    """
    Mark a borrowed book as returned.

    This endpoint updates the borrowing record to indicate that the book has been returned.
    It also increases the available quantity of the book by one.

    Args:
        borrowing_id (int): The ID of the borrowing record to be marked as returned.
        db (Session, optional): The database session dependency.

    Raises:
        HTTPException: If the borrowing record is not found, a 404 Not Found error is raised.

    Returns:
        dict: A message indicating the successful return of the book.
    """

    db_borrowing = borrowing_crud.return_book(db, borrowing_id=borrowing_id)
    if db_borrowing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrowing record not found"
        )
    # Increase the book quantity
    book = book_crud.get_book(db, book_id=db_borrowing.book_id)
    book.available_quantity = book.available_quantity + 1
    db.add(book)
    db.commit()
    return {"message": "Book returned successfully"}
