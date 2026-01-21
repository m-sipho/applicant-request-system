from fastapi import HTTPException, status
from schemas import CreateUser, RoleEnum
from auth.utils import Hash
from sqlalchemy.orm import Session
import os
from models import User
from auth.utils import Hash

def create_applicant_user(request: CreateUser, db: Session):
    # Check for existing user
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Check if the password has at least 8 characters
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password needs 8+ characters"
        )
    
    # Create new applicant
    new_user = User(
        name=request.name,
        email=request.email,
        password=Hash.get_password_hashed(request.password),
        role=RoleEnum.applicant
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def create_staff_user(request: CreateUser, db: Session):
    # Avoid duplicates
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    
    # Check if the password has at least 8 characters
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password needs 8+ characters"
        )
    
    # Create staff
    new_staff = User(
        name=request.name,
        email=request.email,
        password=Hash.get_password_hashed(request.password),
        role=RoleEnum.staff
    )

    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    return new_staff

def create_admin_user(secret: str, request: CreateUser, db: Session):
    if secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid secret")

    # Check if admin already exists
    admin_exists = db.query(User).filter(User.role == RoleEnum.admin).first()
    if admin_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin already exists")
    
    # Check if the password has at least 8 characters
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password needs 8+ characters"
        )
    
    admin = User(
        name=request.name,
        email=request.email,
        password=Hash.get_password_hashed(request.password),
        role=RoleEnum.admin
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {"message": "Admin created"}