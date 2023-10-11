import os


def display_welcome_message():
    print("Welcome to the Expense Tracking App!")

def display_error_message(message):
    print(f"Error: {message}")

def display_success_message(message):
    print(f"Success: {message}")

def prompt_for_csv_file():
    return input("Please specify the location of the CSV file: ")

def specify_bank():
    return input("Source of Bank Statement [Bank Name]: ")

def display_transaction(transaction):
    print("Transaction Details:")
    print(f"Date: {transaction['Date']}")
    print(f"Description: {transaction['Description']}")
    print(f"Amount: {transaction['Amount']:.2f}")
    print(f"Category: {transaction.get('Category', 'Uncategorized')}")

def prompt_for_category():
    return input("Please specify the category for this transaction: ")

# You can add more user interface functions as needed.
