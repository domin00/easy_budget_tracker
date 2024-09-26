import os


'''
Logic driver for automated categorization.
Idea here is to implement a (likely ML) solution that allows for automated category labeling
based on past manually labeled transactions.
'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Load the CSV data
csv_data = pd.read_csv('data/labelled/labelled_santander_2024-07-03_2024-07-31.csv')

# Prepare the features and target
X = csv_data['Description']
y = csv_data['Category']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with TF-IDF vectorizer and Multinomial Naive Bayes classifier
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB()),
])

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Print the classification report
print(classification_report(y_test, y_pred))

# Function to predict category for new transactions
def predict_category(description):
    return model.predict([description])[0]

# Example usage
new_transaction = "LIDL BUDOWLANA Warszawa"
predicted_category = predict_category(new_transaction)
print(f"Predicted category for '{new_transaction}': {predicted_category}")