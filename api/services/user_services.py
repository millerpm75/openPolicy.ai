from sqlalchemy.orm import Session
from database.models import User, UserCreate
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def get_password_hash(password: str) -> str:
#     """Hash the password before storing it."""
#     if not password:
#         logger.error("❌ ERROR: Password is empty or None!")
#         hashed = pwd_context.hash(password)
#         logger.debug(f"✅ Hashed Password: {hashed}")  # Log hashed password
#     return hashed

# class UserCreate(BaseModel):
#     email: str
#     name: str
#     password: str
#     policy_interests: List[str] = []
#     preferred_jurisdictions: List[str] = []

def create_user(db: Session, user: UserCreate):
    print(f"DEBUG: Raw Password Before Hashing: {user.password}")

    # Ensure password is NOT already hashed
    if user.password.startswith("$2b$12$"):  # bcrypt hashes always start with this prefix
        raise ValueError("ERROR: Password is already hashed. Do not hash it again!")

    hashed_password = pwd_context.hash(user.password)
    print(f"DEBUG: Hashed Password at Registration: {hashed_password}")  # <-- Add this
    db_user = User(
        email=user.email,
        name=user.name,
        password_hash=hashed_password,  # Make sure this is assigned correctly
        policy_interests=user.policy_interests,
        preferred_jurisdictions=user.preferred_jurisdictions
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db_user.name = user.name
    db_user.policy_interests = user.policy_interests
    db_user.preferred_jurisdictions = user.preferred_jurisdictions
    db.commit()
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()

def list_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
