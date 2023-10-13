import sqlite3

def display_all_transactions():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('data/database/my_bank_app.db')
        cursor = conn.cursor()

        # Query to select all transactions from the Transactions table
        cursor.execute('SELECT * FROM Transactions')

        # Fetch all transactions
        transactions = cursor.fetchall()

        if transactions:
            print("List of Transactions:")
            for transaction in transactions:
                print(f"TransactionID: {transaction[0]}")
                print(f"Date: {transaction[1]}")
                print(f"Description: {transaction[2]}")
                print(f"Amount: {transaction[3]:.2f}")
                print(f"CategoryID: {transaction[4]}")
                print(f"Month: {transaction[5]}\n")
        else:
            print("No transactions found.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    display_all_transactions()
