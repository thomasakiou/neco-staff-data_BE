from pydantic import BaseModel
from typing import Optional
from src.domain.user import UserRole

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

class StaffDTO(BaseModel):
    id: Optional[int] = None
    fileno: str
    full_name: str
    remark: Optional[str] = None
    conr: Optional[str] = None
    station: Optional[str] = None
    qualification: Optional[str] = None
    sex: Optional[str] = None
    dob: Optional[str] = None
    dofa: Optional[str] = None
    dopa: Optional[str] = None
    doan: Optional[str] = None
    rank: Optional[str] = None
    state: Optional[str] = None
    lga: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class UserDTO(BaseModel):
    id: int
    username: str
    role: UserRole
    staff_id: Optional[int]

    class Config:
        from_attributes = True
