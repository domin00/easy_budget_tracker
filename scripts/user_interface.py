import os
import pandas as pd
import json

supported_categories = json.load('data/categories.json')
CATEGORY_MAP = {index+1: category for index, category in enumerate(supported_categories)}


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
        print(idx+1, ": ", category)

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
