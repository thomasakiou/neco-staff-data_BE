import pandas as pd
from datetime import datetime
from typing import List, Dict
from src.domain.staff import Staff

class ExcelLoader:
    @staticmethod
    def load_staff_from_excel(file_path: str) -> List[Staff]:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='latin-1')
        else:
            df = pd.read_excel(file_path)
            
        df = df.fillna('')
        
        staff_list = []
        for _, row in df.iterrows():
            data = row.to_dict()
            
            fileno = str(data.get('fileno', '')).strip()
            if not fileno: continue # Skip if no file number
            
            # Pad fileno with leading zeros to 4 digits if numeric
            if fileno.isdigit():
                fileno = fileno.zfill(4)
           
            dob_val = data.get('dob', '')
            dob_str = ""
            if isinstance(dob_val, (pd.Timestamp, datetime)):
                dob_str = dob_val.strftime('%y%m%d')
            elif isinstance(dob_val, str) and len(dob_val) >= 8:
                try:
                    dt = pd.to_datetime(dob_val, dayfirst=True)
                    dob_str = dt.strftime('%y%m%d')
                except:
                    dob_str = dob_val
            else:
                dob_str = str(dob_val)

            staff = Staff(
                id=None,
                fileno=str(fileno),
                full_name=str(data.get('full_name', data.get('name', ''))),
                remark=str(data.get('remark', '')),
                conr=str(data.get('conr', data.get('conraiss', ''))),
                station=str(data.get('station', '')),
                qualification=str(data.get('qualification', '')),
                sex=str(data.get('sex', '')),
                dob=dob_str,
                dofa=str(data.get('dofa', '')),
                dopa=str(data.get('dopa', '')),
                doan=str(data.get('doan', '')),
                rank=str(data.get('rank', '')),
                state=str(data.get('state', '')),
                lga=str(data.get('lga', '')),
                email=str(data.get('email', '')),
                phone=str(data.get('phone', ''))
            )
            staff_list.append(staff)
        return staff_list

    @staticmethod
    def load_partial_staff_data(file_path: str) -> List[Dict]:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='latin-1', dtype=str)
        else:
            df = pd.read_excel(file_path, dtype=str)
            
        df = df.fillna('')
        
        # Valid staff attributes to allow updates for
        valid_fields = {
            'full_name', 'remark', 'conr', 'station', 'qualification', 
            'sex', 'dob', 'dofa', 'dopa', 'doan', 'rank', 'state', 
            'lga', 'email', 'phone'
        }
        
        partial_updates = []
        for _, row in df.iterrows():
            data = row.to_dict()
            
            fileno = str(data.get('fileno', '')).strip()
            if not fileno: continue 
            
            if fileno.isdigit():
                fileno = fileno.zfill(4)
                
            update_data = {'fileno': fileno}
            
            # Helper to process DOB
            def process_dob(val):
                if isinstance(val, (pd.Timestamp, datetime)):
                    return val.strftime('%y%m%d')
                if isinstance(val, str) and len(val) >= 8:
                    try:
                        dt = pd.to_datetime(val, dayfirst=True)
                        return dt.strftime('%y%m%d')
                    except:
                        pass
                return str(val)

            for key, val in data.items():
                clean_key = key.lower().strip()
                # Map some common variations if needed, or rely on strict naming
                if clean_key == 'name': clean_key = 'full_name'
                if clean_key == 'conraiss': clean_key = 'conr'
                
                if clean_key in valid_fields and str(val).strip() != '':
                    if clean_key == 'dob':
                        update_data[clean_key] = process_dob(val)
                    else:
                        update_data[clean_key] = str(val)
            
            if len(update_data) > 1: # If we have more than just fileno
                partial_updates.append(update_data)
                
        return partial_updates
