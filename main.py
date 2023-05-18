import pandas as pd
from tabulate import tabulate


def read_csv(path):
    '''
    This function reads the individual CSV files containing bank statements.
    By using a function it is possible to use the same function for seperate months and allocate data into a database independently.
    INPUT: "Path" -- File Pathway
    OUTPUT: "Data" -- dataframe containing N number of rows with TBD number of columns.
    '''

    df = pd.read_csv(path)
    df2 = df.iloc[: , [1, 2, 5]].copy()
    df2.columns = ['Date','Description','Amount']

    df2['Truncated Description'] = df2['Description'].str.extract(r'PLN(.*)')

    # Fill NaN values with the original strings
    df2['Truncated Description'].fillna(df2['Description'], inplace=True)

    df2['Description'] = df2['Truncated Description']
    del df2['Truncated Description']



    print(df2)
    


path = 'data/historia_2023-05-16_04109025900000000153544523.csv'

read_csv(path)
