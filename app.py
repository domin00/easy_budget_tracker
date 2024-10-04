import json
import streamlit as st
import pandas as pd
import os
from datetime import datetime

from scripts.csv_processor import process_csv
from scripts.app_helper import save_labeled_transactions, filter_by_category
from scripts.analysis import display_transactions_count, display_daily_expenses_and_income  

# Streamlit App
def main():
    st.title("CSV Transactions Processor")

    categories = load_categories()

    tab1, tab2 = st.tabs(["Upload & Process", "Analysis & Visualizations"])

    with tab1:
        uploaded_file = upload_csv_file()

        if uploaded_file is not None:
            date_range = select_date_range()
            bank = select_bank()
            transactions_df = process_transactions(uploaded_file, bank, date_range)
            edited_df = display_transactions(transactions_df, categories)
            handle_user_actions(edited_df)

    with tab2:
        if 'edited_df' in locals():
            st.subheader("Transaction Analysis")
            # Placeholder for analysis and visualizations
            display_transactions_count(edited_df)
            display_daily_expenses_and_income(edited_df)
        else:
            st.info("Please upload and process transactions in the 'Upload & Process' tab first.")

def load_categories():
    with open(os.path.join("data", 'categories.json'), 'r') as file:
        return json.load(file)

def upload_csv_file():
    return st.file_uploader("Upload CSV file", type=["csv"])

def select_date_range():
    start_date = st.date_input("Select start date", value=datetime(2024, 1, 1), min_value=datetime.min, max_value=datetime.max)
    end_date = st.date_input("Select end date", min_value=datetime.min, max_value=datetime.max)
    return start_date, end_date

def select_bank():
    bank_options = ['Revolut', 'UBS', 'UBS Main', 'Santander']
    return st.selectbox("Select bank", bank_options, index=bank_options.index('Santander'))

def process_transactions(uploaded_file, bank, date_range):
    start_date, end_date = date_range
    return process_csv(uploaded_file, bank, start_date, end_date)

def display_transactions(transactions_df, categories):
    st.subheader("Transactions")
    edited_df = st.data_editor(
        transactions_df,
        hide_index=True,
        use_container_width=True,
        disabled=["Date", "Description", "Amount", "Currency", "Bank"],
        column_config={
            "Category": st.column_config.SelectboxColumn(
                "Category",
                help="Transaction category",
                options=categories,
                required=True
            )
        }
    )
    return edited_df

def handle_user_actions(transactions_df):
    
    
    if transactions_df['Category'].isnull().any():
        st.warning("Fill out all the category labels before enabling saving of labeled dataset.")
    else:
        save_dataset = st.button("Save! [Developer Only Use]")
        if save_dataset:
            save_labeled_transactions(transactions_df)

    
    display_transactions_count(transactions_df)






if __name__ == "__main__":
    main()
