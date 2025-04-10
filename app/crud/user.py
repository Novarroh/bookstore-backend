from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).filter(User.role == UserRole.CUSTOMER).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,  # In a real app, hash this password
        role=UserRole.CUSTOMER
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if user.password != password:  # In a real app, verify hashed password
        return None
    return user