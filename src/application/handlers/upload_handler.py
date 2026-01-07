from src.domain.repositories import StaffRepository, UserRepository
from src.infrastructure.loaders.excel_loader import ExcelLoader
from src.domain.user import User, UserRole
from src.infrastructure.security.auth import get_password_hash

class UploadStaffDataHandler:
    def __init__(self, staff_repo: StaffRepository, user_repo: UserRepository):
        self.staff_repo = staff_repo
        self.user_repo = user_repo

    def handle(self, file_path: str, update_existing: bool = True):
        staff_list = ExcelLoader.load_staff_from_excel(file_path)
        for staff in staff_list:
            # Check if staff already exists
            existing = self.staff_repo.get_by_fileno(staff.fileno)
            if existing:
                if update_existing:
                    # Update existing staff
                    staff.id = existing.id
                    self.staff_repo.update(staff)
                # Ensure user exists for existing staff even in append mode if they don't have one
                user = self.user_repo.get_by_username(staff.fileno)
                if not user:
                    new_user = User(
                        id=None,
                        username=staff.fileno,
                        hashed_password=get_password_hash(staff.dob),
                        role=UserRole.STAFF,
                        staff_id=existing.id
                    )
                    self.user_repo.add(new_user)
            else:
                # Add new staff
                new_staff = self.staff_repo.add(staff)
                # Ensure user doesn't already exist before adding
                existing_user = self.user_repo.get_by_username(new_staff.fileno)
                if not existing_user:
                    new_user = User(
                        id=None,
                        username=new_staff.fileno,
                        hashed_password=get_password_hash(new_staff.dob),
                        role=UserRole.STAFF,
                        staff_id=new_staff.id
                    )
                    self.user_repo.add(new_user)
                else:
                    # Update staff_id if it's missing
                    if not existing_user.staff_id:
                        existing_user.staff_id = new_staff.id
                        self.user_repo.update(existing_user)
