from database.db_setup import SessionLocal
from database import models

def seed_baseline_data():
    db = SessionLocal()
    try:
        # 1. Seed the Category
        shoe_category = db.query(models.Category).filter(models.Category.name == "Shoe").first()
        if not shoe_category:
            shoe_category = models.Category(name="Shoe")
            db.add(shoe_category)
            print("Added Category: Shoe")

        # 2. Seed the Source
        mp_source = db.query(models.Source).filter(models.Source.name == "MountainProject").first()
        if not mp_source:
            mp_source = models.Source(name="MountainProject", base_url="https://www.mountainproject.com")
            db.add(mp_source)
            print("Added Source: MountainProject")

        db.commit()
        print("✅ Database successfully seeded!")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_baseline_data()
