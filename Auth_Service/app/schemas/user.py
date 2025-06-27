from pydantic import BaseModel, EmailStr,constr
from enum import Enum

class UserRole(str,Enum):
    user = "user"
    vendor = "vendor"
    admin = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password:constr(min_length=8, max_length=128)
    role: UserRole = UserRole.user

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    is_verified: bool

    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token:str
    token_type :str ="bearer"

class EmailVerification(BaseModel):
    email: EmailStr
    code: str