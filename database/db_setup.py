import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Load db URL or default to local file if no URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local_data.db")

# Create engine (connection to db)
# check_same_thread is only needed for SQLite
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create Session Factory to communicate with db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
