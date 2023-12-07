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


@bp.route('/')
def index():

    return render_template('ba_landing_page.html')



# HELPER FUNCTIONS FOR INITALIZATION NEEDS

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


def load_category_map():

    # Category label map
    file_path = os.path.join(current_app.static_folder, 'categories.json')
    with open(file_path, 'r') as file:
        supported_categories = json.load(file)
    CATEGORY_MAP = {index+1: category for index, category in enumerate(supported_categories)}

    return CATEGORY_MAP


# DEMO APP FUNCTIONALITIES

@bp.route('/upload_statement_free', methods=('GET', 'POST'))
def upload_statement_free():
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
            session['uploaded_df'] = df.to_dict('list')
            print(df.keys())

            flash('File uploaded successfully!')
            
            return redirect(url_for('budget_assistant.transactions_free'))
        
        except Exception as e:
            flash(f'Error processing the file: {str(e)}')

    return render_template('upload_statement.html', form=form)

@bp.route('/transactions_free', methods=['GET', 'POST'])
def transactions_free():

    CATEGORY_MAP = load_category_map()

    if session.get('transactions'):
        transactions_dict = session.get('transactions')
        transactions = pd.DataFrame(transactions_dict)

    else:
        transactions = get_all_transactions()  # Assuming get_all_transactions retrieves all transactions
        transactions['Category'] = transactions['CategoryID'].map(CATEGORY_MAP)
        transactions['True Amount'] = transactions.apply(convert_to_base, axis=1)

        transactions_dict = transactions.to_dict('list')
        
        session['transactions'] = transactions_dict
    # TRANSACTIONS = transactions
    
    
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
    

exchange_rates_cache = {}

def convert_to_base(row):
    # Define the base currency (assuming it's CHF, change it accordingly)
    base_currency = 'CHF'

    # Create a CurrencyRates object
    c = CurrencyRates()

    # convert to datetime
    date = pd.to_datetime(row['Date'])
    date_time = dt.datetime.combine(date, dt.datetime.min.time())

    # Check if the exchange rate is already cached
    if (row['Currency'], date_time) not in exchange_rates_cache:
        try:
            # Fetch and cache the exchange rate
            date = pd.to_datetime(row['Date'])
            date_time = dt.datetime.combine(date, dt.datetime.min.time())
            exchange_rates_cache[(row['Currency'], date_time)] = c.get_rate(row['Currency'], base_currency, date_time)

        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    # Apply the conversion using the cached rate
    return round(row['Amount'] * exchange_rates_cache[(row['Currency'], date_time)], 2)

    
# Routes for private use of the app, not public simplified.

@bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():

    CATEGORY_MAP = load_category_map()

    # if session.get('transactions'):
    #     transactions = session.get('transactions')

    # else:
    transactions = get_all_transactions()  # Assuming get_all_transactions retrieves all transactions
    transactions['Category'] = transactions['CategoryID'].map(CATEGORY_MAP)
    transactions['True Amount'] = transactions.apply(convert_to_base, axis=1)

    transactions_dict = transactions.to_dict('list')
    
    session['transactions'] = transactions_dict
    # TRANSACTIONS = transactions
    
    
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
        transactions_dict = session.get('transactions')
        transactions = pd.DataFrame(transactions_dict)

    else:
        transactions = get_all_transactions()  # Assuming get_all_transactions retrieves all transactions
        transactions['Category'] = transactions['CategoryID'].map(CATEGORY_MAP)
        transactions['True Amount'] = transactions.apply(convert_to_base, axis=1)
        
        transactions_dict = transactions.to_dict('list')
        
        session['transactions'] = transactions_dict

    summary_table, totals = process_transactions(transactions)

    # plot_url = generate_line_plot(summary_table)
    
    # Pass the summary_table to the template
    return render_template('summary.html', summary_table=summary_table, totals=totals)#, plot_url=plot_url)

@bp.route('/upload_statement', methods=('GET', 'POST'))
@login_required
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