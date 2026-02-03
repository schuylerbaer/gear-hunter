from sqlalchemy.orm import Session
from database.models import Alert

def create_alert(db: Session, user_id: int, brand: str = None, model: str = None, size: str = None):
    alert = Alert(
            user_id=user_id,
            target_brand=brand,
            target_model=model,
            target_size=size,
            is_active=True
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def get_user_alerts(db: Session, user_id: int):
    return db.query(Alert).filter(Alert.user_id == user_id).all()

def toggle_alert(db: Session, user_id: int):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.is_active = not alert.is_active
        db.commit()
        db.refresh(alert)
    return alert

def delete_alert(db: Session, alert_id: int):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        db.delete(alert)
        db.commit()
        return True
    return False
