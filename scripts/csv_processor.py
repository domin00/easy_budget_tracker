import os
import scripts.utils
import pandas as pd

def parse_csv(csv_path, bank_type):

    #TODO: remove the need for an additional function just to call a function
    transactions = scripts.utils.read_csv(csv_path, bank_type)
    transactions['Date'] = pd.to_datetime(transactions['Date']).dt.date


    # add category column 
    # transactions['Category'] = "Uncategorized"

    return transactions

# Function to process CSV based on date range and display transactions
def process_csv(file, bank, start_date, end_date):
    df = parse_csv(file, bank)
    
    # Filter transactions based on date range
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df[mask]
    filtered_df['Category'] = None
    
    return filtered_df