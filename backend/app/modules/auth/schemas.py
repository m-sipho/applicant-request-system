from pydantic import BaseModel, EmailStr
from enum import Enum

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class RoleEnum(str, Enum):
    applicant = "applicant"
    staff = "staff"
    admin = "admin"

class RegisterUser(BaseModel):
    id: int
    email: str
    role: RoleEnum

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None