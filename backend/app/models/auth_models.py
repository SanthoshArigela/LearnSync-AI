from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str
    role: str = "student"  # "student" or "faculty"

class UserModel(BaseModel):
    id: str
    name: str
    email: str
    role: str  # "student" or "faculty"

class LoginResponse(BaseModel):
    authenticated: bool
    user: Optional[UserModel] = None
    message: Optional[str] = None
