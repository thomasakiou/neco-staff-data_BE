from fastapi import FastAPI
from src.infrastructure.database.db import engine, Base, SessionLocal
from src.infrastructure.database.models import UserModel
from src.domain.user import UserRole
from src.infrastructure.security.auth import get_password_hash
from src.infrastructure.config import get_settings
from src.api.routers import auth, admin, staff

# Create database tables
Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(title="NECO Staff Data Management System")

# Initialize Super Admin
def create_super_admin():
    db = SessionLocal()
    try:
        admin_user = db.query(UserModel).filter(UserModel.username == settings.SUPER_ADMIN_USERNAME).first()
        if not admin_user:
            new_admin = UserModel(
                username=settings.SUPER_ADMIN_USERNAME,
                hashed_password=get_password_hash(settings.SUPER_ADMIN_PASSWORD),
                role=UserRole.ADMIN
            )
            db.add(new_admin)
            db.commit()
            print(f"Super Admin created: {settings.SUPER_ADMIN_USERNAME}")
        else:
            print("Super Admin already exists")
    finally:
        db.close()

create_super_admin()

# Include Routers
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(staff.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to NECO Staff Data API"}
