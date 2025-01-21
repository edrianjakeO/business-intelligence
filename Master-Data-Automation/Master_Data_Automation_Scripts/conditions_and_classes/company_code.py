import pandas as pd


class CompanyCode:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict

    
    def input_code(self):
        df1 = self.sheets_dict['1-Customers']
        df2 = self.sheets_dict['2-Contacts']
        df3 = self.sheets_dict['3-Sales_reps']
        df1.columns = df1.columns.str.lower()
        df2.columns = df2.columns.str.lower()
        df3.columns = df3.columns.str.lower()

        df1['companycode'] = df1.apply(
            lambda row: '0210' if pd.notnull(row['search_term1']) else row['companycode'],
            axis=1
            )
        df1['title'] = df1['title'].apply(
            lambda row: str(row).zfill(4) if pd.notnull(row) else None
        )
        df2['companycode'] = df2.apply(
            lambda row: '0210' if pd.notnull(row['title']) else row['companycode'],
            axis=1
            )
        df3['companycode'] = df3.apply(
            lambda row: '0210' if pd.notnull(row['title']) else row['companycode'],
            axis=1 
            )
        
        # AJ - AM column must be in 24hr format
        df1['pickuphrsfrom'] = df1['pickuphrsfrom'].apply(
            lambda row: str(int(row)).zfill(6) if pd.notnull(row) else None
            )
        # str(int(row).zfill(6) = converts the int to string and fill zeroes
        
        df1['pickuphrsto'] = df1['pickuphrsto'].apply(
            lambda row: str(int(row)).zfill(6) if pd.notnull(row) else None
            )
        
        df1['deliverhrsfrom'] = df1['deliverhrsfrom'].apply(
            lambda row: str(int(row)).zfill(6) if pd.notnull(row) else None
            )
        
        df1['deliverhrsto'] = df1['deliverhrsto'].apply(
            lambda row: str(int(row)).zfill(6) if pd.notnull(row) else None
            )
        
        # title for the sales-rep sheet
        df3['title'] = df3['title'].apply(
            lambda row: str(int(row)).zfill(4) if pd.notnull(row) else None
            )
        


        return self.sheets_dict