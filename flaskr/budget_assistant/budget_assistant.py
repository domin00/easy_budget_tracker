from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from scripts.database import *

bp = Blueprint('budget_assistant', __name__, template_folder='ba_templates')

# Category label map
with open('static/categories.json', 'r') as file:
    supported_categories = json.load(file)
CATEGORY_MAP = {index+1: category for index, category in enumerate(supported_categories)}

@bp.route('/budget_assistant/start')
def index():

    return render_template('start.html')

@bp.route('/budget_assistant/transactions')
@login_required
def transactions():
    transactions = get_all_transactions()
    transactions['Category'] = transactions['CategoryID'].map(CATEGORY_MAP)
    
    return render_template('transactions.html', transactions= round(transactions, 2))

@bp.route('/budget_assistant/summary', methods=('GET', 'POST'))
@login_required
def summary():
    transactions = get_all_transactions()

    summary_table, totals = process_transactions(transactions)

    # plot_url = generate_line_plot(summary_table)
    
    # Pass the summary_table to the template
    return render_template('summary.html', summary_table=summary_table, totals=totals)#, plot_url=plot_url)

def process_transactions(transactions):

    transactions['Month'] = pd.to_datetime(transactions['Date']).dt.strftime('%Y-%m')
    transactions['Category'] = transactions['CategoryID'].map(CATEGORY_MAP)
    # transactions['Amount'] = round(transactions['Amount'], 2)
    
    # Group transactions by Month and CategoryID, summing up Amount
    # Create a summary table with CategoryID as rows, Month as columns, and sum of Amount as values
    summary_table = pd.pivot_table(transactions, values='Amount', index='Category', columns='Month', aggfunc='sum', fill_value=0)
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