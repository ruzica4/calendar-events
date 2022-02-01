from flask import render_template
from flask_login import login_required

from . import home_blueprint as home


@home.route('/')
def homepage():
    return render_template('home/index.html',
                           title='Welcome to the Calendar WebApp!')


@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html',
                           title='Welcome to the dashboard!')
