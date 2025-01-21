import pandas as pd
import re


class removeSpecChar:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict

    def special_charRemove(self):

        df = self.sheets_dict['1-Customers']
        df.columns = df.columns.str.upper()

        df['STREET1'] = df['STREET1'].str.replace(r'[^A-Za-z0-9 ]+', '', regex=True)
                
        return self.sheets_dict
