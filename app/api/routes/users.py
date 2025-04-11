from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.user import User, UserCreate, LoginRequest, UserUpdate, RoleUpdate
from app.crud import user as user_crud
from app.models.user import UserRole

router = APIRouter()

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    return user_crud.create_user(db=db, user=user)

@router.post("/login", response_model=User)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, email=login_data.email, password=login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return {"id": user.id,  "first_name": user.first_name, "last_name": user.last_name,"email": user.email, "role": user.role, "is_active": user.is_active}

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}/role", response_model=User)
def update_user_role(user_id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    admin_id = role_update.admin_id
    admin = user_crud.get_user(db, user_id=admin_id)
    if admin is None or admin.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can update user roles"
    )
    user_update = UserUpdate(role=role_update.role)
    db_user = user_crud.update_user(db, user_id=user_id, user=user_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user