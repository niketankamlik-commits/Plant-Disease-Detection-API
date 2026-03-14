from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt
import uuid
from datetime import datetime, timedelta

def get_password_hash(password: str) -> str:
    # bcrypt requires bytes, so we encode the string
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# API Key Operations
def get_api_keys(db: Session, user_id: int):
    return db.query(models.APIKey).filter(models.APIKey.user_id == user_id).all()

def create_api_key(db: Session, user_id: int, user_name: str):
    # Generate a unique key
    new_key = str(uuid.uuid4()).replace("-", "")
    
    expires_at = None
    # If not admin 'niket', set expiry to 2 months (60 days)
    if user_name.lower() != "niket":
        expires_at = datetime.utcnow() + timedelta(days=60)
    
    db_key = models.APIKey(
        key=new_key,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key

def validate_api_key(db: Session, key: str):
    db_key = db.query(models.APIKey).filter(models.APIKey.key == key).first()
    if not db_key or not db_key.is_active:
        return None
    
    # Check if expired
    if db_key.expires_at and db_key.expires_at < datetime.utcnow():
        return None
        
    return db_key.owner
