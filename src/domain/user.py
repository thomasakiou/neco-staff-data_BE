from enum import Enum
from typing import Optional
from dataclasses import dataclass

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"

@dataclass
class User:
    id: Optional[int]
    username: str  # fileno for staff, 'admin' for superadmin
    hashed_password: str
    role: UserRole
    staff_id: Optional[int] = None
