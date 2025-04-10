from app.database import Base, engine
from app.models.user import User
from app.models.book import Book
from sqlalchemy import inspect

def main():
    # Get an inspector to check if tables exist
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    # Print existing tables
    if existing_tables:
        print(f"Existing tables in database: {', '.join(existing_tables)}")
    else:
        print("No existing tables found in database")
    
    print("Creating any missing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables are now up to date!")

if __name__ == "__main__":
    main()