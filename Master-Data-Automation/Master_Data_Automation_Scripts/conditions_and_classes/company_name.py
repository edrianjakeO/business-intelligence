import pandas as pd
import csv
import re

class CompanyName:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict
        self.company_abbrev_dict = self.load_company_abbrev('company_abbrev.csv')  # Load CSV on initialization
        self.abbrev_set = set(self.company_abbrev_dict.values())

    def load_company_abbrev(self, file_path):
        company_abbrev_dict = {}
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                company = row['company'].upper()
                abbrev = row['abbrev'].upper()
                company_abbrev_dict[company] = abbrev
        return company_abbrev_dict
    
    
    
    def get_abbrev(self, company):
        if pd.notnull(company):
            # Iterate over the abbreviation dict
            for idx, (key, value) in enumerate(self.company_abbrev_dict.items()):
                # If the key (company name in the dictionary) is found in the input company string
                if key in company.upper():
                    # Replace the word in the string with the abbreviation
                    company = company.upper().replace(key, value)
            return company  # Return the modified company name (or the original if no match found)
        return company 
    
    def clean_specChar(self, specialChar):
        
        if pd.notnull(specialChar) and isinstance(specialChar, str):
            specialChar = re.sub(r'[.,]', ' ', specialChar)
        return specialChar  
    
    def update_states(self):
        df = self.sheets_dict['1-Customers']
        df.columns = df.columns.str.upper()  

        df['SEARCH_TERM1'] = df.apply(
            lambda row: self.get_abbrev(row['NAME1'])
            if pd.notnull(row['NAME1'])
            else row['SEARCH_TERM1'],  
            axis=1
        )

        df['SEARCH_TERM1'] = df['SEARCH_TERM1'].apply(lambda x: self.clean_specChar(x))
        df['NAME1'] = df['NAME1'].apply(lambda x: self.clean_specChar(x))
        
        return self.sheets_dict
