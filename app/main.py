from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import CreateRequest, CreateUser, RoleEnum, Token, ShowRequest
from .request_types import REQUEST_TYPE_RULES
from . import models, database
from .database import engine
from sqlalchemy.orm import Session
from .hashing import Hash
from typing import Annotated
from .token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from .oauth2 import get_current_user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Applicant Request System API. Go to /docs for API documentation."}

@app.post("/request", status_code=status.HTTP_201_CREATED, response_model=ShowRequest)
def create_request(request: CreateRequest, current_user: Annotated[CreateUser, Depends(get_current_user)], db: Session = Depends(database.get_db)):
    rules = REQUEST_TYPE_RULES.get(request.request_type)
    if current_user.role != RoleEnum.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can create requests"
        )

    if not rules:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported request type"
        )
    required_fields = rules["required"]
    
    for field_name, field_type in required_fields.items():
        if field_name not in request.metadata:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {field_name}"
            )
        if not isinstance(request.metadata[field_name], field_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type of field: {field_name}"
            )
    
    new_request = models.Request(type=request.request_type, description=request.description, data=request.metadata, owner_id=current_user.id)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request: CreateUser, db: Session = Depends(database.get_db)):
    # Check for existing user
    existing = db.query(models.User).filter(models.User.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.get_password_hashed(request.password),
        role=RoleEnum.student
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)) -> Token:
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
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