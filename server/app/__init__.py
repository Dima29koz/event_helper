from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

from server.config import BaseConfig

db = SQLAlchemy()
login_manager = LoginManager()
sio = SocketIO()
migrate = Migrate()
mail = Mail()


def create_app(config: BaseConfig) -> Flask:
    """
    Creates app and register Blueprints

    :returns: app
    :rtype: Flask
    """
    app = Flask(
        __name__,
        template_folder=config.TEMPLATE_FOLDER,
        static_folder=config.STATIC_FOLDER,
    )
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.test_request_context():
        db.create_all()

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    sio.init_app(app, logger=config.LOGGER, manage_session=config.MANAGE_SESSION)

    return app
