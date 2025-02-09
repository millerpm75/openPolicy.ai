# db_connection.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Set up the database connection
engine = create_engine(DATABASE_URL, echo=True, future=True, isolation_level="AUTOCOMMIT")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Function to get a new database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
