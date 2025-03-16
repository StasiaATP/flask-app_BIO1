from flask import Flask
from app.config import Config
from app.models import db, User  # Import User model!
from app import teilnehmer_routes
from flask_login import LoginManager
from app.db_setup import setup_database

def create_app():
    app = Flask(__name__, template_folder="../templates")  # ✅ Set correct template path
    app.config.from_object(Config)
    app.register_blueprint(teilnehmer_routes.routes)

    setup_database(app)

    # ✅ Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    # ✅ This function tells Flask-Login how to load a user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
