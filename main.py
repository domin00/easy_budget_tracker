import pandas as pd
import difflib


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

    return df2

def process_data(data):

    classes = [
                "Food",
                "Gifts",
                "Health/medical",
                "Home",
                "Transportation",
                "Personal",
                "Utilities",
                "Travel",
                "Sports/Fitness",
                "Other",
                "Hobbies",
                "Investments",
                "Entertainment"
                ]
    
    df = data

    # add category column to populate
    df['Category'] = pd.Series(dtype=str)

    # iterate through transaction rows to asign them categories
    for index, row in df.iterrows():

        print(row)
        x = input("Category: ")


        x_a = difflib.get_close_matches(x, classes, 1, 0.3)[0]


        row['Category'] = x_a

        df.at[index, "Category"] = x_a

    ## TO DO
    # print the updated transactions with the categories and ask for confirmation
    # allow to toggle between potential options --> CONFIRM, EDIT, etc.


    df_out = df

    return df_out










    


path = 'data/historia_2023-05-16_04109025900000000153544523.csv'

data = read_csv(path)

df_out = process_data(data)
