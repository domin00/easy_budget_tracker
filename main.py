from utils import read_csv, process_data
import pandas as pd
import os
import numpy as np
import scripts.database as database
import csv
import scripts.user_interface as user_interface
import scripts.csv_processor as csv_processor
import scripts.categorization as categorization

### KEY FUNCTIONALITIES
# CHECK IF BANK STATEMENT ALREADY ADDED TO MAIN DATABASE
# APPEND DATAFRAME TO DATABASE
# SPLIT DATAFRAME OUTPUT INTO TRANSACTIONS AND INCOMES

def parse_args():


    args = 1

    return args


# bank statement paths
santander_data = 'data/historia_2023-05-16_04109025900000000153544523.csv'
ubs_data = 'data/invoice.csv'

# processing
data_sant = read_csv(santander_data, 'santander')
data_ubs = read_csv(ubs_data, 'ubs')
new_data = pd.concat([data_sant, data_ubs], ignore_index=True)


def main():
    # Welcome message and user interaction
    user_interface.display_welcome_message()
    csv_file_path = user_interface.prompt_for_csv_file()
    bank_type     = user_interface.specify_bank()

    # Check if the specified CSV file exists
    if not os.path.isfile(csv_file_path):
        user_interface.display_error_message("CSV file not found.")
        return

    # # Parse the CSV file and perform custom processing
    # transactions = csv_processor.parse_csv(csv_file_path)

    # # List each transaction to the user for categorization
    # for transaction in transactions:
    #     user_interface.display_transaction(transaction)
    #     category = user_interface.prompt_for_category()
    #     transaction['Category'] = category

    # Store transaction list in the database
    database.db_init()
    # database.insert_transactions(transactions)

    # user_interface.display_success_message("Transactions have been categorized and stored.")

if __name__ == "__main__":
    main()
