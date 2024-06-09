from dotenv import load_dotenv
import os
import gspread
import json
import pandas as pd

load_dotenv()

class DriveBot:
    def __init__(self):
        self.gc = gspread.service_account(filename="analise-de-dados-com-python-f6000f4f3130.json")

    def get_data(self):
        sheet_key = os.getenv("SHEETS_KEY")
        sh = self.gc.open_by_key(sheet_key)
        worksheet = sh.sheet1
        dataframe = pd.DataFrame(worksheet.get_all_values())
        return dataframe