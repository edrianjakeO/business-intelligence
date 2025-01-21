import csv
import pandas as pd


class TimezoneInput:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict
        self.state_timezone_map = self.load_timezone_state('state_timezone.csv')  # Load CSV on initialization

    def load_timezone_state(self, file_path):
        state_timezone_map = {}
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                state = row['state'].upper()
                timezone = row['timezone'].upper()
                state_timezone_map[state] = timezone
        return state_timezone_map
    
    def get_timezone(self, state):
        return self.state_timezone_map.get(state, '')
    
    def update_timezones(self):
        df = self.sheets_dict['1-Customers']
        df.columns = df.columns.str.upper()

        df['TIMEZONE'] = df.apply(
            lambda row: self.get_timezone(
                row['STATE']) 
                if pd.notnull(row['STATE']) 
                else row['TIMEZONE'], 
            axis=1
            )

        return self.sheets_dict
