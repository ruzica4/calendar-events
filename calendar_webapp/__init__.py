from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from config import app_config

# db initialization code
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    # loading config files will be relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Bootstrap(app)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to continue.'
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app, db)

    from calendar_webapp import models

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .home import home_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/home')

    from .user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden.')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page not found.')

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Internal server error.')

    return app
