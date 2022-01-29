import datetime

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
        return '<User> {}'.format(self.username)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer(), primary_key=True)
    event_title = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    events = db.relationship('EventType', backref='event', lazy='dynamic')

    # modified_time - maybe it should be implemented

    def __init__(self, event_title=""):
        self.event_title = event_title

    def __repr__(self):
        return '<Event {}>'.format(self.event_name)


class EventType(db.Model):
    __tablename__ = 'event_type'
    id = db.Column(db.Integer(), primary_key=True)
    event_description = db.Column(db.String(255))
    date_of_event = db.Column(db.DateTime, nullable=False)
    type = db.Column('type', db.String(50))

    event_id = db.Column(db.Integer(), db.ForeignKey('event.id'))

    def __repr__(self):
        return f'<{self.__class__.__name__}(event_date={self.event_date})>'

    __mapper_args__ = {
        'polymorphic_identity': 'event_type',
        'polymorphic_on': type
    }


class Meeting(EventType):
    __tablename__ = 'meeting'
    event_type_id = db.Column(db.Integer(), ForeignKey='event_type.if')

    __mapper_args__ = {
        'polymorphic_identity': 'meeting',
    }


class Birthday(EventType):
    __tablename__ = 'birthday'
    event_type_id = db.Column(db.Integer(), ForeignKey='event_type.if')

    __mapper_args__ = {
        'polymorphic_identity': 'birthday',
    }


class Reminder(EventType):
    __tablename__ = 'reminder'
    event_type_id = db.Column(db.Integer(), ForeignKey='event_type.if')

    __mapper_args__ = {
        'polymorphic_identity': 'reminder',
    }
