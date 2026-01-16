from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from ..schemas import Token
from .. import models, database, hashing, token
from datetime import timedelta

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)) -> Token:
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not hashing.Hash.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid password"
        )
    
    # Generate a jwt token and return it
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")