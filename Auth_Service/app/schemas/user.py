from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str,Enum):
    user = "user"
    vendor = "vendor"
    admin = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password:str
    role: UserRole = UserRole.user

class UserOut(BaseModel):
    id:int
    email:EmailStr
    role:UserRole

    class Config:
        orm_model =True
class Token(BaseModel):
    access_token:str
    token_type :str ="bearer"