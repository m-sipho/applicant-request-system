from fastapi import APIRouter, status, Depends
from typing import Annotated
from ..oauth2 import get_current_user
from ..schemas import CreateUser, UserOut

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_current_user(current_user: Annotated[CreateUser, Depends(get_current_user)]):
    return current_user