from sqlalchemy.orm import Session
from database.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str):
    hashed_pw = pwd_context.hash(password)
    db_user = User(email=email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, new_email: str = None, new_password: str = None):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    if new_email:
        user.email = new_email
    if new_password:
        user.hashed_password = pwd_context.hash(new_password)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
