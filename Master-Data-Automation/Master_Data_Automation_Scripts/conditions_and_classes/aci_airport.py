import csv
import pandas as pd

class ACIAirport:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict
        self.aci_airport_dict, self.aci_zone_dict = self.load_aci_basis('aci_basis.csv')  
        self.aci_set = set(self.aci_airport_dict.keys())  
        self.aci_zone_set = set(self.aci_zone_dict.keys())  

    def load_aci_basis(self, file_path):
        aci_airport_dict = {}
        aci_zone_dict = {}
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                postal = row['POSTALCODE'].strip().zfill(5)  # Ensure ZIP is treated as string with leading zeros
                country = row['COUNTRY'].strip().upper()  
                state = row['STATE'].strip().upper()  
                aci_airport = row['ACI_AIRPORT'].strip().upper()  
                aci_zone = row['ACI_ZONE'].strip().upper()
                key = (postal, country, state)  # Create a key from (postal, country, state)
                aci_airport_dict[key] = aci_airport
                aci_zone_dict[key] = aci_zone
        return aci_airport_dict, aci_zone_dict

    def get_aci(self, postal, country, state):
        """Fetches the ACI_AIRPORT based on postal, country, and state."""
        key = (postal, country, state)
        return self.aci_airport_dict.get(key, " ")

    def get_aci_zone_set(self, postal, country, state):
        """Fetches the ACI_ZONE based on postal, country, and state."""
        key = (postal, country, state)
        return self.aci_zone_dict.get(key, " ")

    def update_aci_airport(self):
        df = self.sheets_dict['1-Customers']
        df.columns = df.columns.str.upper()

        
        df['ACI_AIRPORT'] = df.apply(
            lambda row: self.get_aci(
                str(row['POSTALCODE']).strip().zfill(5),  
                str(row['COUNTRY']).strip().upper(), 
                str(row['STATE']).strip().upper() 
            ) if pd.notnull(row['POSTALCODE']) and pd.notnull(row['COUNTRY']) and pd.notnull(row['STATE'])
            else row['ACI_AIRPORT'],  # Return the existing value if any of the fields are null
            axis=1
        )

        df['ACI_ZONE'] = df.apply(
            lambda row: self.get_aci_zone_set(
                str(row['POSTALCODE']).strip().zfill(5),  
                str(row['COUNTRY']).strip().upper(),  
                str(row['STATE']).strip().upper() 
            ) if pd.notnull(row['POSTALCODE']) and pd.notnull(row['COUNTRY']) and pd.notnull(row['STATE'])
            else row['ACI_ZONE'], 
            axis=1
        )

        return self.sheets_dict
