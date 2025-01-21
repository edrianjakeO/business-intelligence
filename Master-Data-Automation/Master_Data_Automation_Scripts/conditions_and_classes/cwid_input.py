import pandas as pd
import csv

class CwidInsert:
    def __init__(self, sheets_dict, file_name):
        self.sheets_dict = sheets_dict
        self.sales_org_dict = self.load_sales_org('sales_org.csv')  # Load org list from csv
        self.file_name = file_name

    def load_sales_org(self, file_path):
        sales_org_dict = {}
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                org = str(row['Org']).upper()
                brand = str(row['Brand']).upper()
                plant = str(row['Plant']).upper()
                sales_org_dict[org] = brand, plant
        return sales_org_dict

    def process_filename(self):
        return str(self.file_name).split("_")[0]

    def insert_org(self):
        df = self.sheets_dict['1-Customers']
        df1 = self.sheets_dict['3-Sales_reps']
        df2 = self.sheets_dict['2-Contacts']
        df.columns = df.columns.str.lower()
        df1.columns = df1.columns.str.lower()
        df2.columns = df2.columns.str.lower()

        station_name = self.process_filename()

        # Condition functions
        def apply_org_six_char_match(row): #  A17SAT(station_name) = A17SAT(org)
            matches = [org for org in self.sales_org_dict if station_name[:6] == org[:6]]
            if matches:
                return f"{matches[0][:3]}-{row}"  # return A17
            return row

        def apply_org_starts_with(row): # AI7(station_name) = A17(org)
            matches = [org for org in self.sales_org_dict if station_name.startswith(org)]
            if matches:
                return f"{matches[0][:3]}-{row}"  # return A17
            return row
        
        #sample statio_name = B92ATL, AGEDFW = A51
        # DFW,AGE,1051 if DFW of station_name = org, returns brand[0] and plant[2:]
        def apply_brand_plus_plant(row, brand, plant):
            matches = [org for org in self.sales_org_dict if station_name[3:7] == org[:3]]
            if matches:
                return f"{brand[:1]}{plant[2:4]}-{row}"
            return row

        def apply_org_matches_first_three(row): # A17SAT[:3](station_name) = org[:3]
            matches = [org for org in self.sales_org_dict if station_name[3:7] == org[:3]]
            if matches:
                return f"{matches[0][3:]}-{row}"  # return SAT
            return row

        


        # def apply_org_matches_lastthree(row): # A17SAT(SAT) = org
        #     # Check if last three characters of station_name match any org in sales_org_list
        #     matches = [org for org in self.sales_org_dict if station_name[3:6] == org]
        #     if matches:
        #         return f"{matches[0]}-{row}"  # Use matching org as prefix
        #     return row
        
    
       
        def update_cwid(row):
            brand = self.sales_org_dict.get(station_name[3:7], ('NF', 'NF'))[0] 
            plant = self.sales_org_dict.get(station_name[3:7], ('NF', 'NF'))[1]

            updated_row = apply_org_six_char_match(row)
            # if updated_row == row:
            #     updated_row = apply_org_matches_lastthree(row)
            if updated_row == row:
                updated_row = apply_org_starts_with(row)
            if updated_row == row:
                updated_row = apply_brand_plus_plant(row, brand, plant)
            if updated_row == row:
                updated_row = apply_org_matches_first_three(row)
            return updated_row

        # Apply the update_cwid function to the 'cwid' column conditionally
        df['cwid'] = df['cwid'].apply(lambda row: update_cwid(row) if pd.notnull(row) else row)
        df1['cwid'] = df1['cwid'].apply(lambda row: update_cwid(row) if pd.notnull(row) else row)
        df2['idnumber'] = df2['idnumber'].apply(lambda row: update_cwid(row) if pd.notnull(row) else row)


        return self.sheets_dict
