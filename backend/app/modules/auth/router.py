from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import CreateUser, RegisterUser, RoleEnum, Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from utils import Hash
from service import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta
from users.models import User
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not Hash.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid password"
        )
    
    # Generate a jwt token and return it
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")