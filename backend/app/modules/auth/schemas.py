from pydantic import BaseModel, EmailStr
from users.schemas import RoleEnum

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class RegisterUser(BaseModel):
    id: int
    email: str
    role: RoleEnum

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None