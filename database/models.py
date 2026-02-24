from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ==========================================
# 1. IDENTITY & STRUCTURE
# ==========================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    alerts = relationship("Alert", back_populates="user")
    matches = relationship("Match", back_populates="user")

class Category(Base):
    """e.g., 'Shoe', 'Rope', 'Cam'"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Source(Base):
    """e.g., 'MountainProject', 'eBay'"""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    base_url = Column(String, nullable=False)

# ==========================================
# 2. INGESTION (The Scraper's Findings)
# ==========================================
class Listing(Base):
    """The raw web post container."""
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    url = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True) # Good for debugging AI mistakes
    status = Column(String, default="Active") # Active, Sold, Removed
    date_found = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, default=datetime.utcnow) # For our "Sold" check

    items = relationship("Item", back_populates="listing")

class Item(Base):
    """A specific piece of gear inside a Listing."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    listing = relationship("Listing", back_populates="items")
    attributes = relationship("ItemAttribute", back_populates="item")
    images = relationship("Image", back_populates="item")

class ItemAttribute(Base):
    """The Key-Value Dictionary (e.g., Brand: Scarpa, Size: 41)"""
    __tablename__ = "item_attributes"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    key = Column(String, nullable=False, index=True) # e.g., 'brand', 'size'
    value = Column(String, nullable=False, index=True) # e.g., 'scarpa', '41.5'

    item = relationship("Item", back_populates="attributes")

class Image(Base):
    """Stores scraped image URLs."""
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    url = Column(String, nullable=False)

    item = relationship("Item", back_populates="images")

# ==========================================
# 3. INTELLIGENCE & DELIVERY (The User's Desires)
# ==========================================
class Alert(Base):
    """The Watchlist Container."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="alerts")
    criteria = relationship("AlertCriteria", back_populates="alert")

class AlertCriteria(Base):
    """The specific dropdown choices (e.g., Brand: Scarpa)"""
    __tablename__ = "alert_criteria"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False)
    key = Column(String, nullable=False) # e.g., 'brand', 'size'
    value = Column(String, nullable=False) # e.g., 'scarpa', '41.5'

    alert = relationship("Alert", back_populates="criteria")

class Match(Base):
    """Powers the Home Feed and Notification Memory."""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    status = Column(String, default="Unread") # Unread, Read, Archived
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="matches")
    item = relationship("Item")
