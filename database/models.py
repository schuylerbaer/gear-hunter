from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    size = Column(String)
    price = Column(Float, nullable=True)
    url = Column(String, unique=True)
    date_found = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)

    target_brand = Column(String)
    target_model = Column(String)
    target_size = Column(String)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)

    alert_id = Column(Integer, ForeignKey("alerts.id"))
    listing_id = Column(Integer, ForeignKey("listings.id"))

    sent_at = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert")
    alert = relationship("Listing")
