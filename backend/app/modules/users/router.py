from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from schemas import UserOut, CreateUser
from auth.service import get_current_user, require_staff, require_admin
from service import create_staff_user, create_applicant_user, create_admin_user
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ==============================
# Applicants
# ==============================
@router.get("/applicant/me", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_current_active_user(current_user: Annotated[CreateUser, Depends(get_current_user)]):
    return current_user

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_applicant(request: CreateUser, db: Session = Depends(get_db)):
    return create_applicant_user(request=request, db=db)

# ==============================
# Staff
# ==============================
@router.post("/", response_model=UserOut)
async def create_staff(request: CreateUser, current_user: Annotated[CreateUser, Depends(require_admin)], db: Session = Depends(get_db)):
    return create_staff_user(request=request, db=db)

# ==============================
# Admin
# ==============================
bootstrap = APIRouter(
    prefix="/admin",
    tags=["Bootstrap"]
)

@bootstrap.post("/admin")
async def create_admin(secret: str, request: CreateUser, db: Session = Depends(get_db)):
    return create_admin_user(secret=secret, request=request, db=db)