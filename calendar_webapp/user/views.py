import datetime

from flask import render_template, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from . import user_blueprint as user
from .forms import EventForm
from calendar_webapp.models import Event
from .. import db


@user.route('/')
@login_required
def home():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html',
                           events=events)


@user.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    form = EventForm()
    print(form)
    if form.validate_on_submit():
        event = Event(title=form.title.data,
                      description=form.description.data,
                      type=form.type.data,
                      # date_of_event=form.date_of_event,
                      user_id=current_user.id)

        try:
            db.session.add(event)
            db.session.commit()
            flash('Added new event.')

            return redirect(url_for('user.home'))

        except Exception as e:
            flash('There was an error while adding your event: %s' % str(e))
            db.session.rollback()

    events = Event.query.filter_by(id=current_user.id)

    return render_template('user/events.html',
                           events=events,
                           form=form)


@user.route('/reminders')
def get_all_reminders():
    reminders = Event.query.filter_by(id=current_user.id, type='REMINDER').all()

    return render_template('home.html',
                           events=reminders)


@user.route('/meetings')
def get_all_meetings():
    meetings = Event.query.filter_by(id=current_user.id, type='MEETING').all()
    print(meetings)
    return render_template('home.html',
                           events=meetings)


@user.route('/birthdays')
def get_all_birthdays():
    birthdays = Event.query.filter_by(user_id=current_user.id, type='BIRTHDAY').all()
    print(birthdays)
    return render_template('home.html',
                           events=birthdays)
