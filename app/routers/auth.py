from .. import models, oauth2, schemas, utils
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Authentications"]
)

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Username and password are required")
    
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}