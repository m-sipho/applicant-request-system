from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from ..schemas import CreateUser, RoleEnum
from ..oauth2 import get_current_user
from .. import database, models, hashing

router = APIRouter(
    prefix="/staff",
    tags=["Staff"]
)


@router.post("/")
def create_staff(request: CreateUser, current_user: Annotated[CreateUser, Depends(get_current_user)], db: Session = Depends(database.get_db)):
    # Authorize
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create staff accounts"
        )
    
    # Avoid duplicates
    existing = db.query(models.User).filter(models.User.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    
    # Create staff
    new_staff = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.get_password_hashed(request.password),
        role=RoleEnum.staff
    )

    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff