import sqlite3

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('my_bank_app.db')
cursor = conn.cursor()

# Create the Categories table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        CategoryID INTEGER PRIMARY KEY,
        CategoryName TEXT
    )
''')

# Enter the categories if they havent been entered yet
categories = [
    'Housing',
    'Transportation',
    'Food',
    'Healthcare',
    'Debt and Loans',
    'Entertainment',
    'Shopping',
    'Utilities',
    'Savings and Investments',
    'Insurance',
    'Education',
    'Travel',
    'Miscellaneous'
]

# Insert categories with "INSERT OR IGNORE" to prevent duplicates
for category in categories:
    cursor.execute('INSERT OR IGNORE INTO Categories (CategoryName) VALUES (?)', (category,))


# Create the Transactions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATE,
        Description TEXT,
        Amount REAL,
        CategoryID INTEGER,
        Bank TEXT,
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
