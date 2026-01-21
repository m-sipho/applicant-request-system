from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

class RoleEnum(str, Enum):
    applicant = "applicant"
    staff = "staff"
    admin = "admin"
