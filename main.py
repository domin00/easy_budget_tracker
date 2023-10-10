from utils import read_csv, process_data
import pandas as pd
import os
import numpy as np

### KEY FUNCTIONALITIES
# CHECK IF BANK STATEMENT ALREADY ADDED TO MAIN DATABASE
# APPEND DATAFRAME TO DATABASE
# SPLIT DATAFRAME OUTPUT INTO TRANSACTIONS AND INCOMES

def parse_args():


    args = 1

    return args





# excel loader
xl_file = 'finance_database.xlsx'
xl_file = pd.ExcelFile(xl_file)
df_existing = pd.read_excel(xl_file)


# bank statement paths
santander_data = 'data/historia_2023-05-16_04109025900000000153544523.csv'
ubs_data = 'data/invoice.csv'

# processing
data_sant = read_csv(santander_data, 'santander')
data_ubs = read_csv(ubs_data, 'ubs')
new_data = pd.concat([data_sant, data_ubs], ignore_index=True)

new_data.to_excel(xl_file, index=False)
# Append the new DataFrame to the existing Excel file
df_combined = pd.concat([df_existing, new_data], ignore_index=True)

# Save the combined DataFrame to Excel
df_combined.to_excel(xl_file, index=False)

print(data_sant)
