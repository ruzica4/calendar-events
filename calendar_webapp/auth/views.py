from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth_blueprint as auth
from calendar_webapp.auth.forms import LoginForm, RegistrationForm
from calendar_webapp import db
from calendar_webapp.models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')

            # go to the login page
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Registration unsuccessful. User %s: %s' % (str(user), e))
            db.session.rollback()

    # reload registration page
    return render_template('auth/register.html',
                           form=form,
                           title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid email or password.')

    return render_template('auth/login.html',
                           form=form,
                           title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.')

    return redirect(url_for('auth.login'))
