from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from projects.auth import login_required
from projects.db import get_db

from scripts.database import *

bp = Blueprint('home', __name__)

@bp.route('/')
def index():

    return render_template('home/index.html')