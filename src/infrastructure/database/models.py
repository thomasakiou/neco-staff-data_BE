from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.infrastructure.database.db import Base
from src.domain.user import UserRole

class StaffModel(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    fileno = Column(String(100), unique=True, index=True)
    full_name = Column(String(500))
    remark = Column(Text, nullable=True)
    conr = Column(String(100), nullable=True)
    station = Column(String(255), nullable=True)
    qualification = Column(String(500), nullable=True)
    sex = Column(String(50), nullable=True)
    dob = Column(String(100), nullable=True)
    dofa = Column(String(100), nullable=True)
    dopa = Column(String(100), nullable=True)
    doan = Column(String(100), nullable=True)
    rank = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    lga = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(100), nullable=True)

    user = relationship("UserModel", back_populates="staff", uselist=False)

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.STAFF)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)

    staff = relationship("StaffModel", back_populates="user")
