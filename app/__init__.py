from flask import Flask
from app.config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Loads settings from config.py
    db.init_app(app)  # Initializes database
    return app
