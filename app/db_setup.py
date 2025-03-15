"""
db_setup.py – Erstellt die Datenbank und alle Tabellen
--------------------------------------------------------
Dieses Skript initialisiert die SQLite-Datenbank und erzeugt alle
Tabellen, die in `models.py` definiert sind.

Wichtig:
- Es wird KEINE bestehende Datenbank überschrieben.
- Falls `database.db` existiert, werden nur fehlende Tabellen hinzugefügt.
- Dieses Skript sollte NUR einmal ausgeführt werden, um die Datenbank anzulegen.
"""

from flask import Flask
from app.config import Config
from app.models import db  # Importiert das Datenbankobjekt aus models.py

# Flask-App erstellen (wird für den App-Kontext benötigt)
app = Flask(__name__)
app.config.from_object(Config)  # Konfiguration aus config.py laden
db.init_app(app)  # Die SQLAlchemy-Datenbank mit Flask verknüpfen

# Datenbank erstellen (innerhalb des App-Kontexts)
with app.app_context():
    print(" Erstelle die Datenbank und Tabellen...")
    db.create_all()  # Erstellt ALLE Tabellen aus models.py
    print("Datenbank erfolgreich erstellt!")

