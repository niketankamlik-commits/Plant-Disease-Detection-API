from local_db.database import engine, Base
from local_db import models
import os

db_path = "plantcare.db"

def reset_db():
    print("Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables with new SaaS schema...")
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully.")

if __name__ == "__main__":
    reset_db()
