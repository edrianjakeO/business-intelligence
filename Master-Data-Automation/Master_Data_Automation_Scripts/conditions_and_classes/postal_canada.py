import csv
import pandas as pd # type: ignore
import re


class PostalCanada:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict
        self.postal_ca_list = self.load_ca_postal('CA_full.csv')  

    def load_ca_postal(self, file_path):
        postal_ca_list = []
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                postal = re.sub(r"[`()\s]+", "", str(row['postalcode'])).strip().upper()
                postal_ca_list.append(postal)
                
        return postal_ca_list
    
    def check_match(self, postal_code):
            if postal_code in self.postal_ca_list:
                return f"{postal_code[:3]} {postal_code[3:]}"  
            return postal_code 
    
    def postal_checker(self):
        df = self.sheets_dict['1-Customers']
        df.columns = df.columns.str.lower()
        
        if 'postalcode' in df.columns:
            df['postalcode'] = df['postalcode'].apply(
                lambda x: self.check_match(x) if pd.notnull(x) else x
            )

        return self.sheets_dict

       

            


