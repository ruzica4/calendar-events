import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, InputRequired

from calendar_webapp.models import EventType


# TODO add date_of_event field in the form and implemetnt validators
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=256)])
    description = StringField('Description', validators=[Length(max=256)])
    # date_of_event = DateField('Date of the event')
    # date_posted = DateField('Date', format='%Y-%m-%d', default=datetime.datetime.now())
    type = RadioField('Event type', choices=['BIRTHDAY', 'REMINDER', 'MEETING'], validators=[InputRequired()])
    submit = SubmitField('Add event')
