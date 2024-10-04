import os
import scripts.utils
import pandas as pd



# Function to process CSV based on date range and display transactions
def process_csv(file, bank, start_date, end_date):
    df = scripts.utils.read_csv(file, bank)
    
    # Filter transactions based on date range
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df[mask]
    filtered_df['Category'] = None
    
    return filtered_df