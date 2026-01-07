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
