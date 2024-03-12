import json
import streamlit as st
import pandas as pd
import os
from datetime import datetime

from scripts import csv_processor
from scripts.app_helper import save_labeled_transactions


# Function to process CSV based on date range and display transactions
def process_csv(file, bank, start_date, end_date):
    df = csv_processor.parse_csv(file, bank)
    
    # Filter transactions based on date range
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df[mask]
    filtered_df['Category'] = None
    
    return filtered_df

# Function to filter transactions based on category
def filter_by_category(df, category):
    if category == 'All':
        return df
    return df[df['Category'] == category]

# Streamlit App
def main():
    st.title("CSV Transactions Processor")

    # Load the JSON list from the file
    with open('data\\categories.json', 'r') as file:
        categories = json.load(file)

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    

    if uploaded_file is not None:
        # Date range selection
        start_date = st.date_input("Select start date", min_value=datetime.min, max_value=datetime.max)
        end_date = st.date_input("Select end date", min_value=datetime.min, max_value=datetime.max)

        # Bank selection
        bank_options = ['Revolut', 'UBS', 'UBS Main', 'Santander']
        bank = st.selectbox("Select bank", bank_options)

        # Process CSV and display transactions
        transactions_df = process_csv(uploaded_file, bank, start_date, end_date)

        # Display transactions table
        st.subheader("Transactions")
        
        edited_df = st.data_editor(
            transactions_df,
            hide_index=True,
            use_container_width=True,
            disabled=["Date", "Description", "Amount", "Currency", "Bank"],
            column_config={
                "Category": st.column_config.SelectboxColumn(
                    "Category",
                    help = "Transaction category",
                    options = categories,
                    required=True
                )
            }
        )
        transactions_df = edited_df
        
        save_dataset = st.button("Save! [Developer Only Use]")

        if transactions_df['Category'].isnull().any():
            st.warning("Fill out all the category labels before enabling transaction analysis.")
        else:
            analyze = st.button("Analyze Transactions")

        if save_dataset:
            file_path = f'data\\{bank}.csv'
            save_labeled_transactions(transactions_df, file_path)

        if analyze:
            with st.container(border=True):
                st.write(f"**Total Transactions:** {len(transactions_df)}")




if __name__ == "__main__":
    main()
