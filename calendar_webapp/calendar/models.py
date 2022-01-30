import datetime
import enum
import random

from calendar_webapp import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    events = db.relationship('Event', backref='user', lazy='dynamic')

    def __init__(self, username=""):
        self.username = username

    def __repr__(self):
        return '<User: username={}>'.format(self.username)


class EventType(enum.Enum):
    BIRTHDAY = 'Birthday'
    MEETING = 'Meeting'
    REMINDER = 'Reminder'

    event_id = db.Column(db.Integer(), db.ForeignKey('event.id'))

    @classmethod
    def get_random_event(cls):
        return random.choice([EventType.REMINDER, EventType.BIRTHDAY, EventType.MEETING])


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())
    description = db.Column(db.String(255))
    date_of_event = db.Column(db.DateTime, nullable=False)
    remind_me_before_days = db.Column(db.Integer())
    type = db.Column(
        db.Enum(EventType),
        default=EventType.REMINDER,
        nullable=False
    )
    #
    # values_callable=lambda x: [str(member.value) for member in EventType]),
    #                    default=EventType.REMINDER)

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # user = db.relationship('User', back_populates='event')

    # modified_time - maybe it should be implemented

    def __init__(self, title=""):
        self.title = title

    def __repr__(self):
        return '<Event: title={}>'.format(self.title)
