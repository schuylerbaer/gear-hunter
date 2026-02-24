from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.db_setup import get_db
from backend.app.schemas import user as user_schema
from backend.app.schemas import alert as alert_schema
from backend.app.crud import user as user_crud
from backend.app.crud import alert as alert_crud

router = APIRouter()

# ==========================
# USER ENDPOINTS
# ==========================

@router.post("/users/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Check if the email is already taken before bothering the Chef
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return user_crud.create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ==========================
# ALERT ENDPOINTS
# ==========================

@router.post("/users/{user_id}/alerts/", response_model=alert_schema.Alert)
def create_user_alert(
    user_id: int, 
    alert: alert_schema.AlertCreate, 
    db: Session = Depends(get_db)
):
    # Verify the user actually exists first
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return alert_crud.create_alert(db=db, alert=alert, user_id=user_id)

@router.get("/users/{user_id}/alerts/", response_model=List[alert_schema.Alert])
def read_user_alerts(user_id: int, db: Session = Depends(get_db)):
    return alert_crud.get_alerts_by_user(db, user_id=user_id)
