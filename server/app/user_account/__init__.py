from flask import Blueprint

user_account = Blueprint('user_account', __name__)

from . import routes