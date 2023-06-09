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

    df = pd.read_csv(path)

    if bank == 'santander':

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
        df2.loc[:,'Bank'] = 'UBS'

    elif bank == 'ubs':
        
        # only copy key columns
        df2 = df.iloc[:, [3, 4, 6]]
        df2.columns = ['Date','Description','Amount']
        # df2.loc[:,'Description'] = df2['Description'] + " - " + df2['Sector']
        # del df2['Sector']

        df2.loc[:,'Currency'] = 'CHF'
        df2.loc[:,'Bank'] = 'Santander'


    elif bank == 'revolut':

        df2 = None

        df2.loc[:,'Currency'] = 'PLN'
        df2.loc[:,'Bank'] = 'Revolut'

    # unify date formatting


    # remove useless rows without any transaction amounts
    df2 = df2.dropna(subset=['Amount'])

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
