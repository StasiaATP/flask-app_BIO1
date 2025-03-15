class Config:
    SECRET_KEY = 'mysecret'  # Sicherheitsschlüssel für Sessions
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'  # SQLite-Datenbank
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Deaktiviert unnötige Warnungen
