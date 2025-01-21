import pandas as pd


class relationshipsCopy:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict

    def check_col(self, BPID):
        if pd.notnull(BPID) and BPID != '':
            return BPID  
        else:
            return None
    
    def update_relationship(self):
        df = self.sheets_dict['1-Customers']
        df.columns = df.columns.str.upper()
        
        if 'BPID' in df.columns:
            df['BPID'] = df['BPID'].apply(lambda x: str(int(x)) if pd.notnull(x) else None)
    
        df['RELATIONSHIP'] = df['BPID'].apply(
            lambda bpid: self.check_col(bpid) if pd.notnull(bpid) else None
        )
    
        return self.sheets_dict
    




