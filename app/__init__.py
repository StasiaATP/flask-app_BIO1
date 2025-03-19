from flask import Flask
from .config import Config
from .models import db, User  # Import User model!
from .common_routes import common_routes
from .teilnehmer_routes import teilnehmer_routes
from .ausbilder_routes import ausbilder_routes
from flask_login import LoginManager
from .db_setup import setup_database

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates") # Setting correct template & css-file (static--> modal.css) path.
    app.config.from_object(Config)
    app.register_blueprint(common_routes)
    app.register_blueprint(teilnehmer_routes)
    app.register_blueprint(ausbilder_routes)

    setup_database(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    # This function tells Flask-Login how to load a user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
