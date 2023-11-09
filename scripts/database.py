import sqlite3
import pandas as pd

def db_init():
    # Connect to the SQLite database (creates a new file if it doesn't exist)
    conn = sqlite3.connect('data/database/my_bank_app.db')
    cursor = conn.cursor()

    # Create the Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            CategoryID INTEGER PRIMARY KEY,
            CategoryName TEXT
        )
    ''')

    # Enter the categories if they havent been entered yet
    # TODO: remove the categories from here and make it a separate file
    # Check if the Categories table is empty
    cursor.execute('SELECT COUNT(*) FROM Categories')
    count = cursor.fetchone()[0]

    if count == 0:
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
            Date DATE NOT NULL,
            Description TEXT NOT NULL,
            Currency TEXT NOT NULL,
            Bank TEXT NOT NULL,
            Amount REAL NOT NULL,
            CategoryID INTEGER,
            FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
            UNIQUE (Date, Description, Amount, Currency, Bank, CategoryID)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



def insert_transactions(dataframe):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('data/database/my_bank_app.db')

        # Loop through each row in the DataFrame and insert or remove duplicates
        for index, row in dataframe.iterrows():
            # Check if a transaction with the same values already exists in the database
            query = f"SELECT * FROM Transactions WHERE Date = ? AND Description = ? AND Amount = ? AND Currency = ? AND Bank = ? AND CategoryID = ?"
            params = (row['Date'], row['Description'], row['Amount'], row['Currency'], row['Bank'], row['CategoryID'],)
            cursor = conn.execute(query, params)

            # If no matching transaction is found, insert it into the database
            if cursor.fetchone() is None:
                insert_query = "INSERT INTO Transactions (Date, Description, Amount, Currency, Bank, CategoryID) VALUES (?, ?, ?, ?, ?, ?)"
                conn.execute(insert_query, params)
                print(f"Inserted transaction with ID {index} into the 'Transactions' table.")
            else:
                # Remove the duplicate entry
                print(f"Transaction with ID {index} is a duplicate and has been removed.")

        conn.commit()
        print("Data insertion completed.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        conn.close()
        

def get_all_transactions():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('data/database/my_bank_app.db')
        
        # SQL query to select all transactions from the "Transactions" table
        query = "SELECT * FROM Transactions"

        # Load data into a DataFrame using pandas.read_sql
        transactions = pd.read_sql(query, conn)

        # Close the database connection
        conn.close()

        return transactions

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        conn.close()

def save_modified_transactions(transactions):
    
    try:
    # Connect to the SQLite database
        conn = sqlite3.connect('data/database/my_bank_app.db')

        # Iterate through the modified DataFrame 
        for index, row in transactions.iterrows():
            transaction_id = row['TransactionID']
            updated_category_id = row['CategoryID']

            # If the CategoryID has been updated, execute an SQL UPDATE statement
            query = f"UPDATE Transactions SET CategoryID = {updated_category_id} WHERE TransactionID = {transaction_id}"
            conn.execute(query)

        # Commit the changes to the database
        conn.commit()
        print("Data updated and saved to the database successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        conn.close()