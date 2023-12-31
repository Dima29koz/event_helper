import datetime
import os

app_dir = os.path.abspath(os.path.dirname(__file__))


def get_config():
    """

    :return: Returns config object based on `FLASK_ENV` env variable
    """
    match os.environ.get('FLASK_ENV'):
        case 'dev':
            return DevelopmentConfig
        case 'prod':
            return ProductionConfig
        case _:
            raise Exception('wrong flask-env type.')


class BaseConfig:
    """
    Base flask-app config object
    """
    DEBUG = False
    LOGGER = True
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False  # In production, this should always be set to True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)
    JWT_ACCESS_TOKEN_FRESH = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MANAGE_SESSION = True
    TEMPLATE_FOLDER = '../../client/templates'
    STATIC_FOLDER = '../../client/static'
    MAIL_DEBUG = False
    SEND_MAIL = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    APP_HOST = os.environ.get('APP_HOST')
    APP_PORT = os.environ.get('APP_PORT')


class DevelopmentConfig(BaseConfig):
    """
    Development flask-app config object
    """
    DEBUG = True
    SEND_MAIL = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://"
        f"{os.environ.get('DEV_DB_USERNAME')}:"
        f"{os.environ.get('DEV_DB_PASSWORD')}@"
        f"{os.environ.get('DEV_DB_ADDRESS')}/"
        f"{os.environ.get('DEV_DB_NAME')}"
    )


class ProductionConfig(BaseConfig):
    """
    Production flask-app config object
    """
    JWT_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://"
        f"{os.environ.get('DEV_DB_USERNAME')}:"
        f"{os.environ.get('DEV_DB_PASSWORD')}@"
        f"{os.environ.get('DEV_DB_ADDRESS')}/"
        f"{os.environ.get('DEV_DB_NAME')}"
    )