import os

from flask import Flask
from app.extensions import db, migrate
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)  # инициализируем миграции

    from app.routes import main
    app.register_blueprint(main)

    return app