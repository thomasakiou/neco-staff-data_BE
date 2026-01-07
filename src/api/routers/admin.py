from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List
import shutil
import os
from src.api.dependencies import get_staff_repo, get_user_repo, admin_required
from src.application.handlers.upload_handler import UploadStaffDataHandler
from src.application.handlers.staff_handlers import StaffHandler
from src.application.dtos.staff_dto import StaffDTO

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(admin_required)])

@router.post("/upload")
async def upload_sdl(file: UploadFile = File(...), staff_repo = Depends(get_staff_repo), user_repo = Depends(get_user_repo)):
    if not file.filename.endswith(('.xlsx', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx and .csv allowed.")
    
    # Save file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        handler = UploadStaffDataHandler(staff_repo, user_repo)
        handler.handle(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    return {"message": "Data uploaded and synchronized successfully"}

@router.post("/append")
async def append_sdl(file: UploadFile = File(...), staff_repo = Depends(get_staff_repo), user_repo = Depends(get_user_repo)):
    if not file.filename.endswith(('.xlsx', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx and .csv allowed.")
    
    # Save file temporarily
    temp_path = f"temp_append_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        handler = UploadStaffDataHandler(staff_repo, user_repo)
        handler.handle(temp_path, update_existing=False)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    return {"message": "New data appended successfully, duplicates ignored"}

@router.post("/bulk-update")
async def bulk_update_staff(file: UploadFile = File(...), staff_repo = Depends(get_staff_repo)):
    if not file.filename.endswith(('.xlsx', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx and .csv allowed.")
    
    # Save file temporarily
    temp_path = f"temp_bulk_update_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        from src.application.handlers.bulk_update_handler import BulkUpdateHandler
        handler = BulkUpdateHandler(staff_repo)
        result = handler.handle(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    return result
@router.get("/staff", response_model=List[StaffDTO])
async def list_staff(staff_repo = Depends(get_staff_repo), user_repo = Depends(get_user_repo)):
    handler = StaffHandler(staff_repo, user_repo)
    return handler.list_staff()

@router.get("/staff/{staff_id}", response_model=StaffDTO)
async def get_staff(staff_id: int, staff_repo = Depends(get_staff_repo), user_repo = Depends(get_user_repo)):
    handler = StaffHandler(staff_repo, user_repo)
    staff = handler.get_staff(staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.put("/staff/{staff_id}", response_model=StaffDTO)
async def update_staff(staff_id: int, staff_dto: StaffDTO, staff_repo = Depends(get_staff_repo), user_repo = Depends(get_user_repo)):
    staff_dto.id = staff_id
    handler = StaffHandler(staff_repo, user_repo)
    updated = handler.update_staff(staff_dto)
    if not updated:
        raise HTTPException(status_code=404, detail="Staff not found")
    return updated

@router.delete("/staff/delete-all")
async def delete_all_staff(staff_repo = Depends(get_staff_repo), user_repo = Depends(get_user_repo)):
    handler = StaffHandler(staff_repo, user_repo)
    handler.delete_all()
    return {"message": "All staff data and associated user accounts deleted successfully"}
