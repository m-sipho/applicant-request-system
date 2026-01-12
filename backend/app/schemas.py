from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional
from .request_types import RequestType
from enum import Enum
from datetime import datetime

class StatusEnum(str, Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER REVIEW"
    AWAITING_STUDENT_INFO = "AWAITING STUDENT INFO"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"

class RoleEnum(str, Enum):
    applicant = "applicant"
    staff = "staff"
    admin = "admin"

class CreateRequest(BaseModel):
    request_type: RequestType
    description: str
    metadata: Dict[str, Any]

class ShowRequest(BaseModel):
    id: int
    type: RequestType
    status: StatusEnum
    created_at: datetime

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class RegisterUser(BaseModel):
    id: int
    email: str
    role: RoleEnum

class RequestOut(BaseModel):
    id: int
    type: str
    status: str
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    assignee_id: Optional[int] = None
    owner_id: int
    data: Dict[str, Any]

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True