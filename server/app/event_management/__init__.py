from flask import Blueprint

event_management = Blueprint('event_management', __name__, url_prefix='/event_management')

from . import routes, events
