from typing import Dict, Any, List
from src.domain.repositories import StaffRepository
from src.infrastructure.loaders.excel_loader import ExcelLoader

class BulkUpdateHandler:
    def __init__(self, staff_repo: StaffRepository):
        self.staff_repo = staff_repo

    def handle(self, file_path: str) -> Dict[str, Any]:
        partial_data = ExcelLoader.load_partial_staff_data(file_path)
        
        updated_count = 0
        missing_count = 0
        missing_filenos = []
        
        for record in partial_data:
            fileno = record.get('fileno')
            if not fileno: continue
            
            updated_staff = self.staff_repo.update_partial(fileno, record)
            
            if updated_staff:
                updated_count += 1
            else:
                missing_count += 1
                missing_filenos.append(fileno)
                
        return {
            "total_processed": len(partial_data),
            "updated_count": updated_count,
            "missing_count": missing_count,
            "missing_filenos": missing_filenos
        }
