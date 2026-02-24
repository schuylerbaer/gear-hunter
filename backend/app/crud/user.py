from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import models
from backend.app.schemas import user as user_schema

# Set up the password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    """Fetch a single user by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Fetch a user by email (crucial for login and preventing duplicate accounts)."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: user_schema.UserCreate):
    """Hashes the password and saves the new user to the Filing Cabinet."""
    # 1. Hash the plaintext password from the React form
    hashed_password = pwd_context.hash(user.password)
    
    # 2. Package it into the SQLAlchemy Model
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    
    # 3. Save and refresh
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
