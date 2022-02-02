from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import enum
import random

from calendar_webapp import db, login_manager


class User(db.Model, UserMixin):
    """
    creates User table
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(60), unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128))

    events = db.relationship('Event', backref='user', lazy='dynamic')

    @property
    def password(self):
        """
        this should prevent password from being accessed
        """
        return AttributeError('Password can\'t be accessed!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: username={}>'.format(self.username)


# Flask-Login uses this method to
# reload the user object from
# the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class EventType(enum.Enum):
    BIRTHDAY = 'Birthday'
    MEETING = 'Meeting'
    REMINDER = 'Reminder'

    event_id = db.Column(db.Integer(), db.ForeignKey('event.id'))

    @classmethod
    def get_random_event(cls):
        return random.choice([EventType.REMINDER, EventType.BIRTHDAY, EventType.MEETING])


# TODO change date_of_event field properties
class Event(db.Model):
    """
    creates Event table
    """
    __tablename__ = 'event'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())
    description = db.Column(db.String(255))
    date_of_event = db.Column(db.DateTime, default=datetime.datetime.now())
    remind_me_before_days = db.Column(db.Integer())
    type = db.Column(
        db.Enum(EventType),
        default=EventType.REMINDER,
        nullable=False
    )

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    # modified_time - maybe this should be implemented

    # def __init__(self, title=""):
    #     self.title = title

    def __repr__(self):
        return '<Event: title={}>'.format(self.title)
