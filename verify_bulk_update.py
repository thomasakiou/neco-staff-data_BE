import requests
import pandas as pd
import os
import time

# Configuration
BASE_URL = "http://localhost:8000"
FILE_NO = "test_bulk_update_user"
ORIGINAL_PHONE = "08012345678"
NEW_PHONE = "09087654321"

def create_dummy_staff():
    """Create a dummy staff record to update."""
    # We can't access DB directly easily from here without setting up the whole app context,
    # so let's try to use the existing upload endpoint to create a user first.
    
    # Create a small CSV to upload
    df = pd.DataFrame([{
        'fileno': FILE_NO,
        'name': 'Test User',
        'dob': '01/01/90',
        'phone': ORIGINAL_PHONE,
        'email': 'test@example.com'
    }])
    df.to_csv('temp_create.csv', index=False)
    
    # Needs auth... this script assumes we can run it against the local server.
    # But wait, the admin endpoints are protected. Developing a proper integration test 
    # might be hard without a token. 
    # Let's see if we can cheat and use the code directly like a unit test.
    pass

def test_handler_directly():
    """Test the handler logic directly to bypass auth/server issues for quick verification."""
    import sys
    sys.path.append(os.getcwd())
    
    from src.infrastructure.database.db import get_db
    from src.infrastructure.repositories.sqlalchemy_repositories import SqlAlchemyStaffRepository, SqlAlchemyUserRepository
    from src.application.handlers.upload_handler import UploadStaffDataHandler
    from src.application.handlers.bulk_update_handler import BulkUpdateHandler
    from src.domain.staff import Staff
    
    print("Setting up DB session...")
    db_gen = get_db()
    db = next(db_gen)
    
    staff_repo = SqlAlchemyStaffRepository(db)
    user_repo = SqlAlchemyUserRepository(db)
    
    try:
        # 1. Clean up potential leftovers
        print(f"Cleaning up {FILE_NO}...")
        existing = staff_repo.get_by_fileno(FILE_NO)
        if existing:
            # Quick delete hack not available in repo, so we'll just update it to known state
            existing.phone = ORIGINAL_PHONE
            staff_repo.update(existing)
        else:
            # Create user
            print("Creating test user...")
            staff = Staff(
                id=None,
                fileno=FILE_NO,
                full_name="Test User",
                dob="900101",
                phone=ORIGINAL_PHONE
            )
            staff_repo.add(staff)

        # 2. Verify initial state
        staff = staff_repo.get_by_fileno(FILE_NO)
        print(f"Initial phone: {staff.phone}")
        assert staff.phone == ORIGINAL_PHONE
        
        # 3. Create update file
        print("Creating update file...")
        update_df = pd.DataFrame([{
            'fileno': FILE_NO,
            'phone': NEW_PHONE,
            'email': 'new_email@example.com' # Add another field
        }, {
            'fileno': '999999', # Non-existent user
            'phone': '0000000000'
        }])
        update_df.to_csv('temp_update.csv', index=False)
        
        # 4. Run Handler
        print("Running BulkUpdateHandler...")
        handler = BulkUpdateHandler(staff_repo)
        result = handler.handle('temp_update.csv')
        
        print("Result:", result)
        
        # 5. Verify Result
        assert result['updated_count'] == 1
        assert result['missing_count'] == 1
        assert '999999' in result['missing_filenos']
        
        # 6. Verify Database State
        updated_staff = staff_repo.get_by_fileno(FILE_NO)
        print(f"Updated phone: {updated_staff.phone}")
        print(f"Updated email: {updated_staff.email}")
        
        assert updated_staff.phone == NEW_PHONE
        assert updated_staff.email == 'new_email@example.com'
        
        print("SUCCESS: Verification passed!")
        
    finally:
        # Cleanup
        if os.path.exists('temp_update.csv'):
            os.remove('temp_update.csv')
        if os.path.exists('temp_create.csv'):
            os.remove('temp_create.csv')
        db.close()

if __name__ == "__main__":
    test_handler_directly()
