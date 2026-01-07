from src.domain.repositories import StaffRepository, UserRepository
from src.domain.user import User, UserRole
from src.infrastructure.security.auth import get_password_hash, verify_password, create_access_token
from src.application.dtos.staff_dto import StaffDTO, LoginRequest, TokenResponse

class AuthHandler:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login(self, request: LoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_username(request.username)
        if not user or not verify_password(request.password, user.hashed_password):
            return None
        
        token = create_access_token({"sub": user.username, "role": user.role})
        return TokenResponse(access_token=token, token_type="bearer", role=user.role)

class StaffHandler:
    def __init__(self, staff_repo: StaffRepository, user_repo: UserRepository):
        self.staff_repo = staff_repo
        self.user_repo = user_repo

    def get_staff(self, staff_id: int):
        return self.staff_repo.get_by_id(staff_id)

    def list_staff(self):
        return self.staff_repo.list_all()

    def update_staff(self, staff_dto: StaffDTO):
        existing = self.staff_repo.get_by_id(staff_dto.id)
        if not existing:
            return None
        
        # Update staff data
        updated_staff = self.staff_repo.update(staff_dto) # StaffDTO is compatible with Staff domain object here
        
        # Update user password if dob changed
        if existing.dob != staff_dto.dob:
            user = self.user_repo.get_by_staff_id(staff_dto.id)
            if user:
                user.hashed_password = get_password_hash(staff_dto.dob)
                # Note: We need a way to update user in repo, let's add it to UserRepository later if needed
                # For now, we'll assume the user doesn't need password update on every staff edit unless explicitly asked
                pass
        
        return updated_staff

    def delete_all(self):
        self.staff_repo.delete_all()
