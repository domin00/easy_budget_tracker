import os
import streamlit as st
import pandas as pd


def save_labeled_transactions(df, file_path):

    # Check if the file already exists
    if os.path.exists(file_path):
        # Load the existing CSV file
        existing_data = pd.read_csv(file_path)

        # Append the new DataFrame to the existing one
        updated_data = pd.concat([existing_data, df], ignore_index=True)

        # Save the updated DataFrame to the same file
        updated_data.to_csv(file_path, index=False)
    else:
        # If the file doesn't exist, save the DataFrame as a new file
        df.to_csv(file_path, index=False)

    st.success("Saved Succesfully")

# Function to filter transactions based on category
def filter_by_category(df, category):
    if category == 'All':
        return df
    return df[df['Category'] == category]