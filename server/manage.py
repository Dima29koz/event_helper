from dotenv import load_dotenv

load_dotenv()
from server.config import get_config
from server.app import create_app, sio, db

app = create_app(get_config())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
