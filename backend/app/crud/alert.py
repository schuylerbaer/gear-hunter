# backend/app/crud/alert.py
from sqlalchemy.orm import Session
from database import models
from backend.app.schemas import alert as alert_schema

def create_alert(db: Session, alert: alert_schema.AlertCreate, user_id: int):
    # Step 1: Create the "Container" (The Alert row)
    db_alert = models.Alert(
        user_id=user_id,
        category_id=alert.category_id,
        is_active=alert.is_active
    )
    db.add(db_alert)
    db.commit()
    
    # We MUST refresh here! We need the database to tell us what 'id' 
    # it just assigned to db_alert so we can link the criteria to it.
    db.refresh(db_alert) 

    # Step 2: Unpack the dictionary and create the "Rules" (AlertCriteria rows)
    # alert.criteria looks like: {"brand": "Scarpa", "size": "40.5"}
    for key, value in alert.criteria.items():
        db_criteria = models.AlertCriteria(
            alert_id=db_alert.id,  # Linked perfectly using the ID we just refreshed
            key=key,
            value=value
        )
        db.add(db_criteria)
    
    # Commit all the new criteria rows at once
    db.commit()
    
    # Refresh the alert one last time so SQLAlchemy loads the new criteria list 
    # before we send it back to the React frontend.
    db.refresh(db_alert)
    return db_alert

def get_alerts_by_user(db: Session, user_id: int):
    # SQLAlchemy will automatically fetch the linked criteria because 
    # of the `relationship()` we defined in models.py
    return db.query(models.Alert).filter(models.Alert.user_id == user_id).all()

def toggle_alert(db: Session, alert_id: int):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if db_alert:
        # Flip the boolean
        db_alert.is_active = not db_alert.is_active
        db.commit()
        db.refresh(db_alert)
    return db_alert

def delete_alert(db: Session, alert_id: int):
    # SAFETY FIRST: We must delete the child rows (Criteria) before the parent row (Alert)
    # Otherwise, the database will throw a foreign key constraint error.
    db.query(models.AlertCriteria).filter(models.AlertCriteria.alert_id == alert_id).delete()
    
    # Now it is safe to delete the Alert
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if db_alert:
        db.delete(db_alert)
        db.commit()
    return db_alert
