from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import CreateUser, RoleEnum
from .. import models, database, hashing
import os

router = APIRouter(
    prefix="/bootstrap",
    tags=["Bootstrap"]
)


@router.post("/admin")
def create_admin(secret: str, request: CreateUser, db: Session = Depends(database.get_db)):

    # Check if admin already exists
    admin_exists = db.query(models.User).filter(models.User.role == RoleEnum.admin).first()
    if admin_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin already exists")
    
    if secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid secret")
    
    # Check if the password has at least 8 characters
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password needs 8+ characters"
        )
    
    admin = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.get_password_hashed(request.password),
        role=RoleEnum.admin
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {"message": "Admin created"}