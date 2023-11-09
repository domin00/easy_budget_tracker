from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from scripts.database import *

bp = Blueprint('budget_assistant', __name__)


@bp.route('/')
def index():
    transactions = get_all_transactions()
    
    return render_template('budget_assistant/index.html', transactions=transactions)

@bp.route('/summary', methods=('GET', 'POST'))
@login_required
def summary():
    transactions = get_all_transactions()
    transactions['Month'] = pd.to_datetime(transactions['Date']).dt.strftime('%Y-%m')
    
    # Group transactions by Month and CategoryID, summing up Amount
    # Create a summary table with CategoryID as rows, Month as columns, and sum of Amount as values
    summary_table = pd.pivot_table(transactions, values='Amount', index='CategoryID', columns='Month', aggfunc='sum', fill_value=0)
    totals = summary_table.sum(axis=0)
    # Pass the summary_table to the template
    return render_template('budget_assistant/summary.html', summary_table=summary_table, totals=totals)