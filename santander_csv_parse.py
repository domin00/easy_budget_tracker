import pandas as pd
import numpy as np

sant_df = pd.read_csv("data/santander_bank_statement_july.csv")

# only copy key columns
df2 = sant_df.iloc[: , [1, 2, 5]].copy()
df2.columns = ['Date','Description','Amount']

# write script to asign transaction method to each row based on if description contains a keyword
# Define a custom function to assign methods
def assign_method(description):
    if 'PŁATNOŚĆ KARTĄ' in description:
        return 'Card'
    else:
        return 'Transfer'

# Apply the custom function to each row in the Description column
df2['Method'] = df2['Description'].apply(assign_method)

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

print("hi")




