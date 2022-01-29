from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db initialization code

db = SQLAlchemy()


def create_app(object_name):
    app = Flask(__name__)

    db.init_app(app)

    return app
