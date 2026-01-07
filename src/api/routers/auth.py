from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.application.handlers.staff_handlers import AuthHandler
from src.api.dependencies import get_user_repo
from src.application.dtos.staff_dto import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repo = Depends(get_user_repo)):
    handler = AuthHandler(user_repo)
    result = handler.login(LoginRequest(username=form_data.username, password=form_data.password))
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result
