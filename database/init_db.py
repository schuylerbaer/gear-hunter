from database.db_setup import engine
from database.models import Base

def init_db():
    print("Connecting to database...")

    Base.metadata.create_all(bind=engine)

    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()
