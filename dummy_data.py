import os
import logging
import random
from faker import Faker
from flask import Flask

from calendar_webapp import create_app, db
from calendar_webapp.models import User, Event, EventType
from config import DevConfig

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger(__name__)

app = create_app('development')
app.app_context().push()
faker = Faker()


def generate_users(n):
    users = list()
    for i in range(n):
        user = User()
        user.username = faker.name()
        user.email = faker.email()
        user.first_name = faker.first_name()
        user.last_name = faker.last_name()
        user.password = faker.password()
        try:
            db.session.add(user)
            db.session.commit()
            users.append(user)
        except Exception as e:
            log.error('Failed to add user %s: %s.' % (str(user), e))
            db.session.rollback()
    return users


def generate_events(n, users):
    for i in range(n):
        event = Event()
        event.title = faker.sentence()
        event.description = faker.text(max_nb_chars=100)
        event.date_of_event = faker.date_this_century(before_today=False, after_today=True)
        event.remind_me_before_days = random.randrange(1, 365)
        event.type = EventType.get_random_event()
        event.user_id = users[random.randrange(0, len(users))].id
        try:
            db.session.add(event)
            db.session.commit()
        except Exception as e:
            log.error('Failed to add event %s: %s.' % (str(event), e))
            db.session.rollback()


generate_events(100, generate_users(100))
