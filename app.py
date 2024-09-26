import json
import streamlit as st
import pandas as pd
import os
from datetime import datetime

from scripts.csv_processor import parse_csv, process_csv
from scripts.app_helper import save_labeled_transactions, filter_by_category


# Streamlit App
def main():
    st.title("CSV Transactions Processor")

    categories = load_categories()
    uploaded_file = upload_csv_file()

    if uploaded_file is not None:
        date_range = select_date_range()
        bank = select_bank()
        transactions_df = process_transactions(uploaded_file, bank, date_range)
        display_transactions(transactions_df, categories)
        handle_user_actions(transactions_df)

def load_categories():
    with open(os.path.join("data", 'categories.json'), 'r') as file:
        return json.load(file)

def upload_csv_file():
    return st.file_uploader("Upload CSV file", type=["csv"])

def select_date_range():
    start_date = st.date_input("Select start date", min_value=datetime.min, max_value=datetime.max)
    end_date = st.date_input("Select end date", min_value=datetime.min, max_value=datetime.max)
    return start_date, end_date

def select_bank():
    bank_options = ['Revolut', 'UBS', 'UBS Main', 'Santander']
    return st.selectbox("Select bank", bank_options)

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
    save_dataset = st.button("Save! [Developer Only Use]")
    
    if transactions_df['Category'].isnull().any():
        st.warning("Fill out all the category labels before enabling transaction analysis.")
    else:
        analyze = st.button("Analyze Transactions")

    if save_dataset:
        save_labeled_transactions(transactions_df)

    if analyze:
        display_analysis(transactions_df)

def display_analysis(transactions_df):
    with st.container(border=True):
        st.write(f"**Total Transactions:** {len(transactions_df)}")




if __name__ == "__main__":
    main()
