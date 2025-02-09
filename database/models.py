# models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, TIMESTAMP, ForeignKey, Date, ARRAY
from sqlalchemy.orm import relationship
from database.session import Base
import datetime
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal

# Pydantic model for request/response with validation
class UserCreate(BaseModel):
    email: EmailStr  # Ensures email is valid
    name: str = Field(..., min_length=2, description="Name must be at least 2 characters long")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
    policy_interests: List[str] = Field(..., min_items=1, description="List of policy interests must not be empty")
    preferred_jurisdictions: List[Literal["Federal", "State", "Local"]] = Field(
        default=[], description="Jurisdictions must be one of: Federal, State, Local"
    )


class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(String, unique=True, nullable=False)
    title = Column(Text, nullable=False)
    summary = Column(Text)
    status = Column(String)
    sponsor = Column(Text)
    introduced_date = Column(Date)
    last_action = Column(Text)
    full_text_url = Column(Text)
    legislation_level = Column(String, default="federal")
    jurisdiction = Column(String, default="N/A")
    created_at = Column(TIMESTAMP)

class ExecutiveOrder(Base):
    __tablename__ = "executive_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    eo_number = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, default="No summary available")  # <-- Ensure this line exists
    issued_date = Column(String, nullable=True)
    full_text_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<ExecutiveOrder(eo_number='{self.eo_number}', title='{self.title}')>"
    
# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    name = Column(String)
    password_hash = Column(String, nullable=False)
    policy_interests = Column(ARRAY(String))
    preferred_jurisdictions = Column(ARRAY(String))

    # Relationship to user interests
    interests = relationship("UserInterest", back_populates="user", cascade="all, delete")

# User Interests Model
class UserInterest(Base):
    __tablename__ = "user_interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), nullable=False)

    # Relationship back to user
    user = relationship("User", back_populates="interests")


class UserLogin(BaseModel):
    email: EmailStr
    password: str