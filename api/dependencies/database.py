from sqlalchemy.orm import sessionmaker
from database.session import SessionLocal

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
