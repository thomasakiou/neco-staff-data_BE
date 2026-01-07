from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies import get_staff_repo, get_user_repo, get_current_user
from src.application.handlers.staff_handlers import StaffHandler
from src.application.dtos.staff_dto import StaffDTO
from src.domain.user import User

router = APIRouter(prefix="/staff", tags=["staff"])

@router.get("/me", response_model=StaffDTO)
async def get_my_data(current_user: User = Depends(get_current_user), staff_repo = Depends(get_staff_repo)):
    if not current_user.staff_id:
        raise HTTPException(status_code=400, detail="User is not associated with any staff record")
    
    handler = StaffHandler(staff_repo, None)
    staff = handler.get_staff(current_user.staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff record not found")
    return staff

@router.put("/me", response_model=StaffDTO)
async def update_my_data(staff_dto: StaffDTO, current_user: User = Depends(get_current_user), staff_repo = Depends(get_staff_repo), user_repo = Depends(get_user_repo)):
    if not current_user.staff_id:
        raise HTTPException(status_code=400, detail="User is not associated with any staff record")
    
    if staff_dto.id and staff_dto.id != current_user.staff_id:
        raise HTTPException(status_code=403, detail="You can only edit your own data")
    
    staff_dto.id = current_user.staff_id
    # Ensure they don't try to change their own fileno to something else
    # Actually, we should probably restrict what they can edit. 
    # But the prompt says "staff can only view and edit there own row(data)".
    
    handler = StaffHandler(staff_repo, user_repo)
    updated = handler.update_staff(staff_dto)
    if not updated:
        raise HTTPException(status_code=404, detail="Staff not found")
    return updated
