import pandas as pd
from datetime import datetime

def create(data:dict):
    pd.DataFrame(data=data).to_excel(f'../files/specification-{datetime.now().strftime("%d-%m-%y %H:%M:%S")}.xlsx')