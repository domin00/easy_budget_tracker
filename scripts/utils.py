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

        # only copy key columns
        df2 = df.iloc[: , [1, 2, 5]].copy()
        df2.columns = ['Date','Description','Amount']

        # remove clutter
        df2.loc[:,'Truncated Description'] = df2['Description'].str.extract(r'PLN(.*)')

        # Fill NaN values with the original strings
        df2['Truncated Description'].fillna(df2['Description'], inplace=True)
        df2['Description'] = df2['Truncated Description']
        del df2['Truncated Description']

        df2.loc[:,'Currency'] = 'PLN'
        df2.loc[:,'Bank'] = 'Santander'

        # specific post-processing lines
        df2['Amount'] = df2['Amount'].str.replace(',', '.')

    elif bank == 'UBS':
        df = pd.read_csv(path, encoding='unicode_escape', sep=';')
        
        # only copy key columns
        df2 = df.iloc[:, [3, 4, 6]]
        df2.columns = ['Date','Description','Amount']
        # df2.loc[:,'Description'] = df2['Description'] + " - " + df2['Sector']
        # del df2['Sector']

        df2.loc[:,'Currency'] = 'CHF'
        df2.loc[:,'Bank'] = 'UBS'


    elif bank == 'Revolut':
        df = pd.read_csv(path, encoding='unicode_escape', sep=',')
        df = df[df['Amount'] < 0]
        df = df[df['Product'] == 'Current']
        df.loc[df['Type'] == 'EXCHANGE', 'Amount'] = 0
        df['Amount'] = df['Amount'].abs()
        df['Amount'] = df['Amount'] + df['Fee']
        df['Date'] = pd.to_datetime(df['Started Date']).dt.date

        selected_columns = ['Date', 'Amount', 'Description', 'Currency']
        df2 = df[selected_columns].copy()

        # df2.loc[:,'Currency'] = 'PLN'
        df2.loc[:,'Bank'] = 'Revolut'

    elif bank == 'UBS Main':
        df = pd.read_csv(path, encoding='unicode_escape', sep=';', skiprows=9)
        df['Date'] = df['Trade date']
        df['Amount'] = df['Debit'].abs()
        df['Description'] = df['Description1']

        selected_columns = ['Date', 'Amount', 'Description', 'Currency']
        df2 = df[selected_columns].copy()

        df2.loc[:,'Bank'] = 'UBS'

    # unify date formatting


    # remove useless rows without any transaction amounts
    df2 = df2.dropna(subset=['Amount'])
    df2 = df2[df2['Amount'] != 0]

    # remove positive transactions (incoming transfers) to not be accounted in expenses --> accumulate seperately as "INCOME"
    # add the absolut value of transactions (meaning expenses are not a negative number but a positive one that sums up)
    df2['Amount'] = df2['Amount'].apply(lambda x: abs(float(x)))

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
