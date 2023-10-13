from scripts.utils import read_csv, process_data
import pandas as pd
import os
import numpy as np
import csv
import json

import scripts.database as database
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
# data_sant = read_csv(santander_data, 'santander')
# data_ubs = read_csv(ubs_data, 'ubs')
# new_data = pd.concat([data_sant, data_ubs], ignore_index=True)


def add_transactions():
    # Welcome message and user interaction
    user_interface.display_welcome_message()
    csv_file_path = user_interface.prompt_for_csv_file()
    bank_type     = user_interface.specify_bank()

    # Check if the specified CSV file exists
    if not os.path.isfile(csv_file_path):
        user_interface.display_error_message("CSV file not found.")
        return
    
    with open('data/supported_banks.json', 'r') as file:
        supported_banks = json.load(file)

        if bank_type not in supported_banks:
            user_interface.display_error_message("Bank currently not supported.")
            return 

    # # Parse the CSV file and perform custom processing
    transactions = csv_processor.parse_csv(csv_file_path, bank_type)
    transactions = transactions.groupby(['Date', 'Description', 'Currency', 'Bank'], as_index=False)['Amount'].sum()


    # List each transaction to the user for categorization
    with open('data/categories.json', 'r') as file:
        supported_categories = json.load(file)
        category_ids = {category: index+1 for index, category in enumerate(supported_categories)}

        for index, transaction in transactions.iterrows():

            while True:
                user_interface.display_transaction(transaction)
                category = user_interface.prompt_for_category(supported_categories)

                if category == '':
                    transactions.at[index, 'Category'] = "Uncategorized"
                    break

                elif category in supported_categories:
                    transactions.at[index, 'Category'] = category
                    break

                else:
                    print(f"'{category}' is not a supported category. Choose from: {', '.join(supported_categories)}")


        # dataframe post-processing for database
        transactions = transactions[transactions['Category'] != "Uncategorized"]

        transactions["CategoryID"] = transactions['Category'].map(category_ids)

        transactions = transactions.drop("Category", axis = 1)

        # # Sum 'Amount' for rows with the same contents in 'Date' and 'Description' columns
        # summed_df = transactions.groupby(['Date', 'Description'], as_index=False)['Amount'].sum()

        # # Merge the summed DataFrame back with the original DataFrame
        # result_df = transactions.merge(summed_df, on=['Date', 'Description'], how='left', suffixes=('', '_sum'))

        # # Rename the 'Amount_sum' column to 'Amount' and drop the '_sum' column
        # transactions = result_df.drop(columns=['Amount']).rename(columns={'Amount_sum': 'Amount'})

        # amount = transactions.pop('Amount')

        # transactions.insert(2, 'Amount', amount)


    # Store transaction list in the database
    database.db_init()
    database.insert_transactions(transactions)

    user_interface.display_success_message("Transactions have been categorized and stored.")

def view_transactions():
    transactions = database.get_all_transactions()

    if transactions.empty:
        user_interface.display_error_message("No transactions found.")
        return

    user_interface.display_transactions(transactions)



def main():
    while True:
        user_interface.display_menu()
        choice = user_interface.prompt_for_menu_choice()
  
        if choice == "1":
            add_transactions()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            user_interface.display_success_message("Goodbye!")
            break
        else:
            user_interface.display_error_message("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
