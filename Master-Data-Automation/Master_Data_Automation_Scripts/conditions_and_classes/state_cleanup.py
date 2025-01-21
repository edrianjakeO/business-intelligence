import csv
import pandas as pd # type: ignore


class StateAbbrev:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict
        self.state_abbrev_dict = self.load_state_abbrev('state_abbrev.csv')  # Load CSV on initialization
        self.abbrev_set = set(self.state_abbrev_dict.values())

    def load_state_abbrev(self, file_path):
        state_abbrev_dict = {}
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                state = row['state'].upper()
                abbrev = row['abbrev'].upper()
                state_abbrev_dict[state] = abbrev
        return state_abbrev_dict
    
    def get_abbrev(self, state):
        if pd.notnull(state):
            return self.state_abbrev_dict.get(state, state)
        return state
    
    def update_states(self):
        df = self.sheets_dict['1-Customers']
        df.columns = df.columns.str.upper()

        df['STATE'] = df.apply(
            lambda row: self.get_abbrev(
                str(row['STATE']).strip()) 
                if pd.notnull(row['STATE']) 
                and str(row['STATE']).strip() 
                not in self.abbrev_set 
                else row['STATE'],
            axis=1
            )

        return self.sheets_dict
