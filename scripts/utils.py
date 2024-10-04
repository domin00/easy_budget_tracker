import pandas as pd
import difflib
import json

def read_csv(path, bank):
    '''
    This function reads the individual CSV files containing bank statements.
    By using a function it is possible to use the same function for seperate months and allocate data into a database independently.
    INPUT: "Path" -- File Pathway
    OUTPUT: "Data" -- dataframe containing N number of rows with TBD number of columns.
    '''
    pd.options.mode.chained_assignment = None

    

    if bank == 'Santander':
        # Read CSV and select key columns
        sant_df = pd.read_csv(path)
        df2 = sant_df.iloc[:, [1, 2, 5]].copy()
        df2.columns = ['Date', 'Description', 'Amount']

        # Assign transaction method
        df2['Method'] = df2['Description'].apply(lambda x: 'Card' if 'PŁATNOŚĆ KARTĄ' in x else 'Transfer')

        # Clean up description
        df2['Description'] = df2['Description'].str.extract(r'PLN(.*)').fillna(df2['Description'])

        # Set additional information
        df2['Currency'] = 'PLN'
        df2['Bank'] = 'Santander'

        # Create new column classifying transaction as "Expense" or "Income" depending on the amount sign
        # Convert 'Amount' column from string to float
        df2['Amount'] = df2['Amount'].str.replace(',', '.').astype(float)
        df2['Type'] = df2['Amount'].apply(lambda x: 'Expense' if x < 0 else 'Income')
        


    elif bank == 'Revolut':
        # Read CSV and filter data
        df = pd.read_csv(path, encoding='unicode_escape', sep=',')
        df = df[(df['Amount'] < 0) & (df['Product'] == 'Current')]

        # Process Amount
        df.loc[df['Type'] == 'EXCHANGE', 'Amount'] = 0
        df['Amount'] = df['Amount'].abs() + df['Fee']

        # Process Date
        df['Date'] = pd.to_datetime(df['Started Date']).dt.date

        # Select and rename columns
        selected_columns = ['Date', 'Amount', 'Description', 'Currency']
        df2 = df[selected_columns].copy()

        # Add Bank information
        df2.loc[:,'Bank'] = 'Revolut'


    # remove useless rows without any transaction amounts
    df2 = df2.dropna(subset=['Amount'])
    df2 = df2[df2['Amount'] != 0]

    # remove positive transactions (incoming transfers) to not be accounted in expenses --> accumulate seperately as "INCOME"
    # add the absolut value of transactions (meaning expenses are not a negative number but a positive one that sums up)
    df2['Amount'] = df2['Amount'].apply(lambda x: abs(float(x)))

    df2['Date'] = pd.to_datetime(df2['Date'], format='%d-%m-%Y', dayfirst=True).dt.date

    return df2


def process_data(data):

    # Read categories from JSON file
    with open('categories.json', 'r') as file:
        classes = json.load(file)
    
    df = data

    # add category column to populate
    df['Category'] = pd.Series(dtype=str)

    # iterate through transaction rows to asign them categories
    for index, row in df.iterrows():
        
        # print transaction details and asign category
        print(row)
        x = input("Category: ")

        # find closest category match in case of misspelling
        x_a = difflib.get_close_matches(x, classes, 1, 0.3)[0]
        df.at[index, "Category"] = x_a

    ## TO DO
    # print the updated transactions with the categories and ask for confirmation
    # allow to toggle between potential options --> CONFIRM, EDIT, etc.


    df_out = df

    return df_out
