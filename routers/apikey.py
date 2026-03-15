from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from local_db import crud, models, schemas, database
from typing import List

router = APIRouter(prefix="/api/keys", tags=["API Keys"])

# Simple dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate", response_model=schemas.APIKeyOut)
def generate_key(user_id: int, user_name: str, key_name: str, db: Session = Depends(get_db)):
    """
    Generates a new API key for the user.
    Admin 'niket' gets lifetime keys (no expiry) and unlimited keys.
    Others get 2-month expiry and are limited to 5 active keys.
    """
    # Enforce limit for non-admin users
    if user_name.lower() != "niket":
        active_count = crud.count_active_keys(db, user_id=user_id)
        if active_count >= 5:
            raise HTTPException(
                status_code=403, 
                detail="Key limit reached. Regular users are limited to 5 active API keys."
            )
            
    return crud.create_api_key(db, user_id=user_id, user_name=user_name, key_name=key_name)

@router.get("/", response_model=List[schemas.APIKeyOut])
def list_keys(user_id: int, db: Session = Depends(get_db)):
    return crud.get_api_keys(db, user_id=user_id)
