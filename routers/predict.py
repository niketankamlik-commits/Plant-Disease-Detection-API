from fastapi import APIRouter, UploadFile, File, Header, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pred_service import process_image_and_predict
from local_db import database, crud
import io

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/predict")
async def predict_disease(
    file: UploadFile = File(...),
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    API Router handling leaf disease prediction.
    Supports authenticated access via X-API-KEY header.
    """
    user_name = "Guest"
    if x_api_key:
        user = crud.validate_api_key(db, x_api_key)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired API Key")
        user_name = user.name

    try:
        # Read the uploaded image bytes
        contents = await file.read()
        
        # Delegate task to the prediction service
        result = process_image_and_predict(contents)
        
        # Return standardized JSON response
        return JSONResponse(content={
            "success": True,
            "prediction": result.get("label", "Unknown"),
            "confidence": float(result.get("confidence", 0)),
            "recommendation": result.get("recommendation", "No data"),
            "source": user_name
        })
            
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)
