from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(title=settings.APP_NAME)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-status")
def db_status(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return {"db_status": "connection successful", "database": settings.DB_NAME}
    
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to database. Error: {e}"
        )