import os
import scripts.utils
import pandas as pd

def parse_csv(csv_path, bank_type):

    #TODO: remove the need for an additional function just to call a function
    transactions = scripts.utils.read_csv(csv_path, bank_type)
    transactions['Date'] = pd.to_datetime(transactions['Date'], format='%d.%m.%Y', dayfirst=True).dt.date


    # add category column 
    # transactions['Category'] = "Uncategorized"

    return transactions