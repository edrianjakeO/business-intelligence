import pandas as pd
import re

class removeSpecial:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict

    def remove_Special(self):
        sheet_names = ['1-Customers', '2-Contacts']
        

        for sheet_name in sheet_names:
            df = self.sheets_dict[sheet_name]
            df.columns = df.columns.str.upper()

            # Step 1: Clean PHONE column (remove special characters)
            df['PHONE'] = df['PHONE'].apply(lambda x: self.clean_phone(x))
            df['FAX'] = df['FAX'].apply(lambda x: self.clean_phone(x))

                
            self.sheets_dict[sheet_name] = df
        
        return self.sheets_dict

    def clean_phone(self, phone):
        if pd.notnull(phone) and isinstance(phone, str):
           
            phone = re.sub(r'[^0-9]', '', phone)
           
            if len(phone) > 6:
                return f'{phone[:3]} {phone[3:6]} {phone[6:]}'
            return phone
        return phone  
