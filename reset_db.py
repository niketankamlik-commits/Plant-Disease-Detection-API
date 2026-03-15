from local_db.database import engine, Base
from local_db import models
import os

db_path = "plantcare.db"

def reset_db():
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted existing database at {db_path}")
    
    Base.metadata.create_all(bind=engine)
    print("Created all tables with new SaaS schema.")

if __name__ == "__main__":
    reset_db()
