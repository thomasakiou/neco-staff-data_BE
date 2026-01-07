from dataclasses import dataclass
from typing import Optional
@dataclass
class Staff:
    id: Optional[int]
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
