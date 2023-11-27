import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)
from werkzeug.exceptions import abort
import datetime as dt
from forex_python.converter import CurrencyRates

from projects.auth import login_required
from projects.db import get_db
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from scripts.database import *
from scripts.csv_processor import *
from .ba_forms import *

bp = Blueprint('budget_assistant', __name__, template_folder='ba_templates')


@bp.route('/start')
def index():

    return render_template('ba_landing_page.html')

@bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():

    CATEGORY_MAP = load_category_map()

    if session.get('transactions'):
        transactions = session.get('transactions')

    else:
        transactions = get_all_transactions()  # Assuming get_all_transactions retrieves all transactions
        transactions['Category'] = transactions['CategoryID'].map(CATEGORY_MAP)
        transactions['True Amount'] = transactions.apply(convert_to_base, axis=1)
        session['transactions'] = transactions
    
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not end_date:
            end_date = dt.date.today()
            
        if start_date and end_date:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
    
            transactions_filtered = transactions[(pd.to_datetime(transactions['Date']) >= start_date) & (pd.to_datetime(transactions['Date']) <= end_date)]

            return render_template('transactions.html', transactions=round(transactions_filtered, 2))

    
    return render_template('transactions.html', transactions= round(transactions, 2))

@bp.route('/summary', methods=('GET', 'POST'))
@login_required
def summary():
    CATEGORY_MAP = load_category_map()

    if session.get('transactions'):
        transactions = session.get('transactions')

    else:
        transactions = get_all_transactions()  # Assuming get_all_transactions retrieves all transactions
        transactions['Category'] = transactions['CategoryID'].map(CATEGORY_MAP)
        transactions['True Amount'] = transactions.apply(convert_to_base, axis=1)
        session['transactions'] = transactions

    summary_table, totals = process_transactions(transactions)

    # plot_url = generate_line_plot(summary_table)
    
    # Pass the summary_table to the template
    return render_template('summary.html', summary_table=summary_table, totals=totals)#, plot_url=plot_url)

def process_transactions(transactions):
    CATEGORY_MAP = load_category_map()
    transactions['Month'] = pd.to_datetime(transactions['Date']).dt.strftime('%Y-%m')
    transactions['Category'] = transactions['CategoryID'].map(CATEGORY_MAP)
    # transactions['Amount'] = round(transactions['Amount'], 2)
    
    # Group transactions by Month and CategoryID, summing up Amount
    # Create a summary table with CategoryID as rows, Month as columns, and sum of Amount as values
    summary_table = pd.pivot_table(transactions, values='True Amount', index='Category', columns='Month', aggfunc='sum', fill_value=0)
    summary_table = round(summary_table, 2)
    totals = round(summary_table.sum(axis=0), 2)

    return summary_table, totals

# Function to generate a line plot and return it as base64 encoded image
def generate_line_plot(summary_table):
    plt.figure(figsize=(10, 6))
    for category in summary_table.index:
        plt.plot(summary_table.columns, summary_table.loc[category], label=category)

    plt.title('Expenses per Category')
    plt.xlabel('Month')
    plt.ylabel('Expense Amount')
    plt.legend()
    plt.grid(True)
    
    # Save plot to BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode plot image to base64
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    
    return plot_url


def load_category_map():

    # Category label map
    file_path = os.path.join(current_app.static_folder, 'categories.json')
    with open(file_path, 'r') as file:
        supported_categories = json.load(file)
    CATEGORY_MAP = {index+1: category for index, category in enumerate(supported_categories)}

    return CATEGORY_MAP

@bp.route('/upload_statement', methods=('GET', 'POST'))
def upload_statement():
    form = uploadForm()

    if form.validate_on_submit():
        try:
            # Check if 'uploaded_data' already exists in session and remove it
            if 'uploaded_data' in session:
                del session['uploaded_data']
            # Process the uploaded file and bank selection
            file = form.file.data
            bank = form.bank_selection.data

            # Add your processing logic here
            # Read the CSV file into a Pandas DataFrame
            df = parse_csv(file, bank)
            # df = pd.read_csv(file, encoding='unicode_escape', sep=';')

            # Convert DataFrame to dictionary and store in session
            # session['uploaded_data'] = df.to_dict()

            flash('File uploaded successfully!')
            
            return redirect(url_for('budget_assistant.upload_statement'))
        
        except Exception as e:
            flash(f'Error processing the file: {str(e)}')

    return render_template('upload_statement.html', form=form)

@bp.route('/process_statement')
def process_statement():
    # Retrieve the DataFrame from the session
    df_dict = session.get('uploaded_data')

    if df_dict:
        # Convert the dictionary back to a DataFrame
        df = pd.DataFrame.from_dict(df_dict)

        # Perform further processing with the DataFrame
        # ...

        return render_template('budget_assistant/process_statement.html', data=df.to_html())
    else:
        flash('No data found in session. Upload a file first.')
        return redirect(url_for('budget_assistant.upload_statement'))
    

def convert_to_base(row):
    # Define the base currency (assuming it's CHF, change it accordingly)
    base_currency = 'CHF'

    # Create a CurrencyRates object
    c = CurrencyRates()

    try:
        # Get the exchange rate for the specified date and currency
        date = pd.to_datetime(row['Date'])
        date_time = dt.datetime.combine(date, dt.datetime.min.time())
        exchange_rate = c.get_rate(row['Currency'], base_currency, date_time)

        # Convert the price to CHF
        true_amount = row['Amount'] * exchange_rate
        return round(true_amount, 2)  # Rounding to 2 decimal places

    except Exception as e:
        # Handle exceptions (e.g., missing exchange rate data)
        print(f"Error converting currency: {e}")
        return None