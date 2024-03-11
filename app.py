import streamlit as st
import pandas as pd
from datetime import datetime
from scripts import csv_processor

# Function to process CSV based on date range and display transactions
def process_csv(file, bank, start_date, end_date):
    df = csv_processor.parse_csv(file, bank)
    
    # Filter transactions based on date range
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df[mask]
    
    return filtered_df

# Function to filter transactions based on category
def filter_by_category(df, category):
    if category == 'All':
        return df
    return df[df['Category'] == category]

# Streamlit App
def main():
    st.title("CSV Transactions Processor")

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
        st.dataframe(
            transactions_df, 
            width=800,
            hide_index=True)
        
        st.write(f"Total transactions for period: {len(transactions_df)}")


if __name__ == "__main__":
    main()
