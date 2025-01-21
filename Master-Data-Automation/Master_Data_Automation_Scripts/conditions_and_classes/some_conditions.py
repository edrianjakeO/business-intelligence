import pandas as pd

class ExtraCond:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict

    def clean_email(self):
        if '2-Contacts' not in self.sheets_dict:
            raise ValueError("The sheet '2-Contacts' does not exist in the provided data.")

        df = self.sheets_dict['2-Contacts']
        df.columns = df.columns.str.lower()

        if 'email' not in df.columns:
            raise ValueError("The column 'email' does not exist in the sheet.")

   
        first_row = 0  
        last_row = 15000 

        # Loop through rows and convert email values to lowercase
        for index in range(first_row, min(last_row, len(df))):  # Avoid exceeding DataFrame length
            email = df.loc[index, 'email']  # Access the email cell
            if pd.notnull(email) and email != '':
                df.loc[index, 'email'] = str(email).lower()

        self.sheets_dict['2-Contacts'] = df

        return self.sheets_dict
