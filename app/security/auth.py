from fastapi import Header, HTTPException, status
from app.core.config import settings

def check_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Missing authorization header"
        )
    
    parts = authorization.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format. Expected 'Bearer <token>'"
        )
    
    token = parts[1]

    if token != settings.AUTH_TOKEN:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token'"
        )
    
    return True