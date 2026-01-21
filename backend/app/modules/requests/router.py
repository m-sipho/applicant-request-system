from fastapi import APIRouter, status, Depends, HTTPException
from schemas import ShowRequest, CreateRequest, RequestOut
from typing import Annotated, List
from users.schemas import CreateUser
from auth.service import require_applicants, get_current_user
from sqlalchemy.orm import Session
from enums import REQUEST_TYPE_RULES
from models import Request

from ...database import get_db

router = APIRouter(
    prefix="/request",
    tags=["Requests"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowRequest)
async def create_request(request: CreateRequest, current_user: Annotated[CreateUser, Depends(require_applicants)], db: Session = Depends(get_db)):
    # Validate request type
    rules = REQUEST_TYPE_RULES.get(request.request_type)
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
    
    # Create new request
    new_request = Request(type=request.request_type, description=request.description, data=request.metadata, owner_id=current_user.id)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[RequestOut])
async def get_all_requests(current_user: Annotated[CreateUser, Depends(get_current_user)], db: Session = Depends(get_db)):
    requests = db.query(Request).filter(Request.owner_id == current_user.id).all()

    return requests