from sqlalchemy.orm import Session
from typing import List, Optional
from src.domain.staff import Staff
from src.domain.user import User, UserRole
from src.domain.repositories import StaffRepository, UserRepository
from src.infrastructure.database.models import StaffModel, UserModel

class SqlAlchemyStaffRepository(StaffRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: StaffModel) -> Staff:
        return Staff(
            id=model.id,
            fileno=model.fileno,
            full_name=model.full_name,
            remark=model.remark,
            conr=model.conr,
            station=model.station,
            qualification=model.qualification,
            sex=model.sex,
            dob=model.dob,
            dofa=model.dofa,
            dopa=model.dopa,
            doan=model.doan,
            rank=model.rank,
            state=model.state,
            lga=model.lga,
            email=model.email,
            phone=model.phone
        )

    def add(self, staff: Staff) -> Staff:
        model = StaffModel(**{k: v for k, v in staff.__dict__.items() if k != 'id'})
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def get_by_id(self, staff_id: int) -> Optional[Staff]:
        model = self.db.query(StaffModel).filter(StaffModel.id == staff_id).first()
        return self._to_domain(model) if model else None

    def get_by_fileno(self, fileno: str) -> Optional[Staff]:
        model = self.db.query(StaffModel).filter(StaffModel.fileno == fileno).first()
        return self._to_domain(model) if model else None

    def list_all(self) -> List[Staff]:
        models = self.db.query(StaffModel).all()
        return [self._to_domain(m) for m in models]

    def update(self, staff: Staff) -> Staff:
        model = self.db.query(StaffModel).filter(StaffModel.id == staff.id).first()
        if model:
            for k, v in staff.__dict__.items():
                if k != 'id':
                    setattr(model, k, v)
            self.db.commit()
            self.db.refresh(model)
            return self._to_domain(model)
        return None

    def update_partial(self, fileno: str, updates: dict) -> Optional[Staff]:
        model = self.db.query(StaffModel).filter(StaffModel.fileno == fileno).first()
        if model:
            for k, v in updates.items():
                if k != 'id' and k != 'fileno' and hasattr(model, k):
                    setattr(model, k, v)
            self.db.commit()
            self.db.refresh(model)
            return self._to_domain(model)
        return None

    def delete_all(self) -> None:
        self.db.query(StaffModel).delete()
        self.db.query(UserModel).filter(UserModel.role == UserRole.STAFF).delete()
        self.db.commit()

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            hashed_password=model.hashed_password,
            role=model.role,
            staff_id=model.staff_id
        )

    def add(self, user: User) -> User:
        model = UserModel(
            username=user.username,
            hashed_password=user.hashed_password,
            role=user.role,
            staff_id=user.staff_id
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def get_by_username(self, username: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_domain(model) if model else None

    def get_by_staff_id(self, staff_id: int) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.staff_id == staff_id).first()
        return self._to_domain(model) if model else None

    def update(self, user: User) -> User:
        model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if model:
            model.username = user.username
            model.hashed_password = user.hashed_password
            model.role = user.role
            model.staff_id = user.staff_id
            self.db.commit()
            self.db.refresh(model)
            return self._to_domain(model)
        return None
