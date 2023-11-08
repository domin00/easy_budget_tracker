CREATE TABLE IF NOT EXISTS Categories (
            CategoryID INTEGER PRIMARY KEY,
            CategoryName TEXT
        );


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
        );

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);      