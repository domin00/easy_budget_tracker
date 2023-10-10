import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('my_bank_app.db')
cursor = conn.cursor()

# Query to select all categories from the Categories table
query = 'SELECT * FROM Categories'

# Execute the query and fetch all rows
cursor.execute(query)
categories = cursor.fetchall()

# Print the categories
for category in categories:
    print(f'CategoryID: {category[0]}, CategoryName: {category[1]}')

# Close the connection
conn.close()
