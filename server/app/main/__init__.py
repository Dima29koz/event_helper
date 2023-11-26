from flask import Blueprint

main = Blueprint('main', __name__, static_url_path='/', static_folder='../../../docs/build/html')

from . import routes
