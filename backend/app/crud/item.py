from sqlalchemy.orm import Session
from database import models
from backend.app.schemas import item as item_schema

def create_scraped_item(db: Session, item_data: item_schema.ItemCreate):
    # Step 1: Check if we already scraped this exact URL recently.
    # We don't want to create 50 duplicate listings if the scraper runs every 10 minutes.
    db_listing = db.query(models.Listing).filter(models.Listing.url == item_data.url).first()
    
    # If it doesn't exist, create the new Container (Listing)
    if not db_listing:
        db_listing = models.Listing(
            source_id=item_data.source_id,
            url=item_data.url,
            raw_text=item_data.raw_text,
            author=item_data.author
        )
        db.add(db_listing)
        db.commit()
        db.refresh(db_listing)

    # Step 2: Create the specific gear piece (Item) inside that Listing
    db_item = models.Item(
        listing_id=db_listing.id,
        category_id=item_data.category_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Step 3: Loop through the AI's JSON dictionary and save the rules (ItemAttributes)
    # item_data.attributes looks like: {"brand": "La Sportiva", "size": "41"}
    for key, value in item_data.attributes.items():
        db_attribute = models.ItemAttribute(
            item_id=db_item.id,
            key=key,
            value=value
        )
        db.add(db_attribute)
    
    db.commit()
    db.refresh(db_item)
    
    return db_item
