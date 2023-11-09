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

    # add dummy categoryID column holding empty categories
    transactions['CategoryID'] = None



    # Store transaction list in the database
    database.db_init()
    database.insert_transactions(transactions)

    user_interface.display_success_message("Transactions have been categorized and stored.")

def add_categories_to_transactions():
    transactions = database.get_all_transactions()
    transactions = transactions[transactions['CategoryID'].isnull()]

    # Find the lowest and highest date values
    min_date = pd.to_datetime(transactions['Date'], format='%Y-%m-%d', dayfirst=True).min()
    max_date = pd.to_datetime(transactions['Date'], format='%Y-%m-%d', dayfirst=True).max()
    user_interface.display_minmax_date(min_date, max_date)
    start_date, end_date = user_interface.select_transaction_range_prompt()
    transactions = transactions[(transactions['Date'] >= start_date & transactions['Date'] <= end_date)]

    # List each transaction to the user for categorization
    with open('data/categories.json', 'r') as file:
        supported_categories = json.load(file)
        category_ids = {category: index+1 for index, category in enumerate(supported_categories)}

        for index, transaction in transactions.iterrows():

            break_flag = 0

            while True:
                user_interface.display_transaction(transaction)
                category = user_interface.prompt_for_category(supported_categories)

                if category == '':
                    transactions.at[index, 'CategoryID'] = "Uncategorized"
                    break

                elif category in supported_categories:
                    transactions.at[index, 'CategoryID'] = category_ids[category]
                    break
                
                # TODO : under development
                elif category == '0':
                    break_flag = 1
                    break
                
                elif supported_categories[int(category)] in category_ids.keys():
                    transactions.at[index, 'CategoryID'] = category
                    break

                else:
                    print(f"'{category}' is not a supported category. Choose from: {', '.join(supported_categories)}")
            
            if break_flag == 1:
                print("Exiting category assignment.")
                break


        # dataframe post-processing for database
        transactions = transactions[transactions['CategoryID'] != "Uncategorized"]

        transactions = transactions.dropna(subset=['CategoryID'])

    database.save_modified_transactions()





def view_transactions():
    transactions = database.get_all_transactions()

    if transactions.empty:
        user_interface.display_error_message("No transactions found.")
        return

    user_interface.display_view_menu()
    choice = user_interface.prompt_for_view_menu_choice()

    if choice == "1":
        view_all_by_category(transactions)
    elif choice == "2":
        view_all_by_month(transactions)
    elif choice == "3":
        sum_by_category(transactions)
    elif choice == "4":
        user_interface.display_transactions(transactions)
    else:
        user_interface.display_error_message("Invalid choice. Please select a valid option.")

def view_all_by_category(transactions):
    # Get unique categories
    categories = transactions['CategoryID'].unique()

    # Display categories and prompt for selection
    user_interface.display_categories(categories)
    selected_category = user_interface.prompt_for_category_selection(categories)

    # Filter transactions by selected category
    category_transactions = transactions[transactions['CategoryID'] == selected_category]

    # Display transactions for the selected category
    user_interface.display_transactions(category_transactions)

def view_all_by_month(transactions):
    # Extract months from the 'Date' column
    transactions['Month'] = pd.to_datetime(transactions['Date']).dt.strftime('%Y-%m')

    # Get unique months
    months = transactions['Month'].unique()

    # Display months and prompt for selection
    user_interface.display_months(months)
    selected_month = user_interface.prompt_for_month_selection(months)

    # Filter transactions by selected month
    month_transactions = transactions[transactions['Month'] == selected_month]

    # Display transactions for the selected month
    user_interface.display_transactions(month_transactions)

def sum_by_category(transactions):
    # Extract months from the 'Date' column
    transactions['Month'] = pd.to_datetime(transactions['Date'], dayfirst=True).dt.strftime('%Y-%m')

    # specify daterange for desired summary
    
    summed_transactions = transactions.groupby(['Month', 'CategoryID'])['Amount'].sum().reset_index()
    #group by month and categoryID to get summary

    user_interface.display_category_month_totals(summed_transactions)







# TODO:
# def remove_transactions()
# def view_transactions_in_category()



def main():
    while True:
        user_interface.display_menu()
        choice = user_interface.prompt_for_menu_choice()
  
        if choice == "1":
            add_transactions()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            add_categories_to_transactions()
        elif choice == "0":
            user_interface.display_success_message("Goodbye!")
            break
        else:
            user_interface.display_error_message("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
