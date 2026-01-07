from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.staff import Staff
from src.domain.user import User

class StaffRepository(ABC):
    @abstractmethod
    def add(self, staff: Staff) -> Staff:
        pass

    @abstractmethod
    def get_by_id(self, staff_id: int) -> Optional[Staff]:
        pass

    @abstractmethod
    def get_by_fileno(self, fileno: str) -> Optional[Staff]:
        pass

    @abstractmethod
    def list_all(self) -> List[Staff]:
        pass

    @abstractmethod
    def update(self, staff: Staff) -> Staff:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass

class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_staff_id(self, staff_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass
