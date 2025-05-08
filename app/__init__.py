from flask import Flask
from .config import Config
from .routes import main  # <- импортируем объект Blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Регистрируем Blueprint
    app.register_blueprint(main)

    return app