from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Any
from .request_types import RequestType
from enum import Enum

class StatusEnum(str, Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER REVIEW"
    AWAITING_STUDENT_INFO = "AWAITING STUDENT INFO"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"

class RoleEnum(str, Enum):
    student = "student"
    staff = "staff"
    admin = "admin"

class CreateRequest(BaseModel):
    request_type: RequestType
    description: str
    metadata: Dict[str, Any]

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None