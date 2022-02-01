from flask import Blueprint

home_blueprint = Blueprint(
    'home',
    __name__,
    template_folder='/home'
)

from . import views
