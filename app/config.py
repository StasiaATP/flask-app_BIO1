import os

class Config:
    SECRET_KEY = 'mysecret'  # Sicherheitsschlüssel für Sessions
    BASEDIR = os.path.abspath(os.path.dirname(__file__))  # Absolute path
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, '../instance/database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
