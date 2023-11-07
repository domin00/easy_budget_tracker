import os
import pandas as pd
import json

with open('data/categories.json', 'r') as file:
    supported_categories = json.load(file)
CATEGORY_MAP = {index+1: category for index, category in enumerate(supported_categories)}
CATEGORY_MAP['Uncategorized'] = 'Uncategorized'


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
    print(f"Category: {transaction.get('CategoryID', 'Uncategorized')}")

def prompt_for_category(supported_categories):
    print("\n")
    for idx, category in enumerate(supported_categories):
        print(idx+1, ": ", CATEGORY_MAP[category])

    return input("Please specify the category for this transaction: ")

def display_menu():
    print("\nMain Menu:")
    print("1. Add New Transactions")
    print("2. View Past Transactions")
    print("3. Exit")

def prompt_for_menu_choice():
    return input("Please select an option (1/2/3): ")

def display_transactions(transactions):

    print("\nList of Transactions:")

    for index, transaction in transactions.iterrows():
        print(f"Transaction {index}:")
        display_transaction(transaction)

def display_view_menu():
    print("View Options:")
    print("1. View by Category")
    print("2. View by Month")

def prompt_for_view_menu_choice():
    choice = input("Enter your choice: ")
    return choice

def display_categories(categories):
    print("Select a category:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {CATEGORY_MAP[category]}")

def prompt_for_category_selection(categories):
    while True:
        choice = input("Enter the number of the category you want to view: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_months(months):
    print("Select a month:")
    for i, month in enumerate(months, start=1):
        print(f"{i}. {month}")

def prompt_for_month_selection(months):
    while True:
        choice = input("Enter the number of the month you want to view: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(months):
                return months[choice - 1]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")
