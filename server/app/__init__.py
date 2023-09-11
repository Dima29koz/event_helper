from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from server.config import BaseConfig

db = SQLAlchemy()
jwt_manager = JWTManager()
sio = SocketIO()
migrate = Migrate()
mail = Mail()
cors = CORS()


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
    jwt_manager.init_app(app)
    mail.init_app(app)

    with app.test_request_context():
        db.create_all()

    from .main import main as main_blueprint
    from .user_account import user_account as user_account_blueprint
    from .event_management import event_management as event_management_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_account_blueprint)
    app.register_blueprint(event_management_blueprint)

    sio.init_app(app, logger=config.LOGGER, manage_session=config.MANAGE_SESSION)
    cors.init_app(app)
    return app
