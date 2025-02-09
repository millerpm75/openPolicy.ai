from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from database.models import UserCreate, User, UserLogin
from api.services.user_services import create_user, get_user, update_user, delete_user, list_users, get_user_by_email
from api.services.auth import get_password_hash, verify_password, create_access_token, get_current_user
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal
from datetime import timedelta
from database.models import UserLogin

router = APIRouter(prefix="/users", tags=["Users"])


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    policy_interests: List[str]
    preferred_jurisdictions: List[str]

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    return create_user(db, user)

@router.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_logged_in_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    return update_user(db, user_id, user)

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    delete_user(db, user_id)
    return {"message": "User deleted successfully"}

@router.post("/users/login")
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = get_user_by_email(db, user_login.email)

    if not db_user:
        print("🔴 User not found in DB")
    else:
        print("✅ User Found:", db_user.email)
        print("🔹 Stored Hash:", db_user.password_hash)
        print("🔹 Password Entered:", user_login.password)

    if not db_user or not verify_password(user_login.password, db_user.password_hash):
        print("❌ Password verification failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("✅ Password verification succeeded!")

    # Generate JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
