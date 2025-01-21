import pandas as pd
import csv

class CwidInsert:
    def __init__(self, sheets_dict, file_name):
        self.sheets_dict = sheets_dict
        self.sales_org_dict = self.load_sales_org('sales_org.csv')  # Load CSV
        self.file_name = file_name

    # Load sales organization from CSV
    def load_sales_org(self, file_path):
        sales_org_dict = {}
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                org = row['Org'].upper()
                brand = row['Brand'].upper()
                sales_org_dict[brand] = org
        return sales_org_dict

    # Extracts the first three characters from the filename
    def process_filename(self):
        return self.file_name[0:3].upper()  # Extract first three letters and convert to uppercase

    # Update CWID based on matched Org or Brand
    def update_cwid(self, station_name):
        # Check if the station_name matches Org or Brand
        for brand, org in self.sales_org_dict.items():
            if station_name == org[0:3]:  # Match with Org
                return org  # Return the entire Org
            elif station_name == brand[0:3]:  # Match with Brand
                return org  # Return the Org associated with the Brand

        return None  # If no match is found

    # Insert organization information into the DataFrame
    def insert_org(self):
        df = self.sheets_dict['1-Customers']
        df.columns = df.columns.str.lower()  # Ensure column names are lowercase

        station_name = self.process_filename()  # Get the first three letters from the filename

        # Update CWID based on the logic described
        df['cwid'] = df.apply(lambda row: self.update_cwid(station_name), axis=1)

        return self.sheets_dict
