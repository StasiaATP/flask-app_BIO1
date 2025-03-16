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

from app import create_app  #  Holt die korrekte Flask-App mit instance_path
from app.models import db    # Importiert das Datenbankobjekt aus models.py

# Erstelle die Flask-App mit der richtigen Konfiguration
app = create_app()

# Datenbank erstellen (innerhalb des App-Kontexts)
with app.app_context():
    print(" Erstelle die Datenbank und Tabellen...")
    db.create_all()  # Erstellt ALLE Tabellen aus models.py
    print("Datenbank erfolgreich erstellt!")

