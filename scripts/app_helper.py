import os
import streamlit as st
import pandas as pd

from scripts.save_labels import save_df_to_csv

'''
Python file to handle collections of streamlit app helping functions. No logic should be written here. 
Code with logic should be called here through functions.
Functions in this file should be written as wrappers, to deliver the logic functions in a decorated manner.
'''

def save_labeled_transactions(df):

    try:
        save_df_to_csv(df)
        st.success("Saved Succesfully")

    except:
        st.warning("Failed to save CSV file.")

# Function to filter transactions based on category
def filter_by_category(df, category):
    if category == 'All':
        return df
    return df[df['Category'] == category]