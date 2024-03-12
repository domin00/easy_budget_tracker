import json
import streamlit as st
import pandas as pd
import os
from datetime import datetime

from scripts import csv_processor


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


        save_dataset = st.button("Save!")

        if save_dataset:
            file_path = 'data\\revolut.csv'

            transactions_df = edited_df

            # Check if the file already exists
            if os.path.exists(file_path):
                # Load the existing CSV file
                existing_data = pd.read_csv(file_path)

                # Append the new DataFrame to the existing one
                updated_data = existing_data.append(transactions_df, ignore_index=True)

                # Save the updated DataFrame to the same file
                updated_data.to_csv(file_path, index=False)
            else:
                # If the file doesn't exist, save the DataFrame as a new file
                transactions_df.to_csv(file_path, index=False)



if __name__ == "__main__":
    main()
