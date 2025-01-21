import pandas as pd
import csv


class StationSO:
    def __init__(self, sheets_dict, file_name):
        self.sheets_dict = sheets_dict
        self.station_so_dict = self.load_station_so('station.csv')  
        self.file_name = file_name

    def load_station_so(self, file_path):
        station_so_dict = {}
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                org = str(row['Full_Org']).strip().upper()
                bp = str(row['BP']).strip().upper()
                station_so_dict[org] = bp
        return station_so_dict

    def get_filename(self):
        return str(self.file_name).split("_")[0]
    
    def check_station(self):

        station_name = self.get_filename().upper()

        for org, bp in self.station_so_dict.items():
            if station_name == org:
                return bp
        return
                

    def insert_station(self):
        df1 = self.sheets_dict['1-Customers']
        df2 = self.sheets_dict['2-Contacts']
        df3 = self.sheets_dict['3-Sales_reps']
        df1.columns = df1.columns.str.lower()
        df2.columns = df2.columns.str.lower()
        df3.columns = df3.columns.str.lower()

        df1['stationso'] = df1.apply(
        lambda row: self.check_station(), axis=1
        )

        df2['stationso'] = df2.apply(
        lambda row: self.check_station(), axis=1
        )

        df3['stationso'] = df3.apply(
        lambda row: self.check_station(), axis=1
        )

        return self.sheets_dict

        

