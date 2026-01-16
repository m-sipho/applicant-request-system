from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import CreateUser, RoleEnum, RegisterUser
from sqlalchemy.orm import Session
from .. import database, models, hashing

router = APIRouter(
    prefix="/register",
    tags=["Register"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RegisterUser)
async def create_user(request: CreateUser, db: Session = Depends(database.get_db)):

    # Check for existing user
    existing = db.query(models.User).filter(models.User.email == request.email).first()
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
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.get_password_hashed(request.password),
        role=RoleEnum.applicant
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user