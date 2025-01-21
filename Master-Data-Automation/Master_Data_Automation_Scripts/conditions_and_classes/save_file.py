import os
import pandas as pd

class SaveFile:
    def __init__(self, sheets_dict, excel_file):
        self.sheets_dict = sheets_dict
        self.excel_file = excel_file

    def save_file(self):
        output_file = os.path.join('cleaned', f"cleaned_file_{os.path.basename(self.excel_file)}")

        # Create a new Excel writer using the openpyxl engine
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for sheet, data in self.sheets_dict.items():
                data.to_excel(writer, sheet_name=sheet, index=False)

        return output_file