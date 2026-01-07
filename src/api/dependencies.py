from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.infrastructure.database.db import get_db
from src.infrastructure.repositories.sqlalchemy_repositories import SqlAlchemyStaffRepository, SqlAlchemyUserRepository
from src.infrastructure.security.auth import decode_access_token
from src.domain.user import UserRole, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_staff_repo(db: Session = Depends(get_db)):
    return SqlAlchemyStaffRepository(db)

def get_user_repo(db: Session = Depends(get_db)):
    return SqlAlchemyUserRepository(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repo)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
