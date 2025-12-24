from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import CreateUser, RoleEnum
from sqlalchemy.orm import Session
from .. import database, models, hashing

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: CreateUser, db: Session = Depends(database.get_db)):

    # Check for existing user
    existing = db.query(models.User).filter(models.User.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create new applicant
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.get_password_hashed(request.password),
        role=RoleEnum.student
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user