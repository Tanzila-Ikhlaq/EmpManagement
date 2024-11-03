# Pydantic models for request/response validation

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Employee(BaseModel):
    name: str = Field(..., min_length=1, description="Name cannot be empty")
    email: EmailStr
    department: str
    role: str

class EmployeeQueryParams(BaseModel):
    department: Optional[str] = None
    role: Optional[str] = None
    page: int = 1
    limit: int = 10

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str