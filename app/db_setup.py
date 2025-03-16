"""
db_setup.py – Erstellt die Datenbank und alle Tabellen
--------------------------------------------------------
Dieses Skript initialisiert die SQLite-Datenbank und erzeugt alle
Tabellen, die in `models.py` definiert sind.

Wichtig:
- Es wird KEINE bestehende Datenbank überschrieben.
- Falls `database.db` existiert, werden nur fehlende Tabellen hinzugefügt.
- Diese funktionen werden bei jedem Start der app aufgerufen (d.h. man muss das Skript nicht manuell ausführen).
"""

from datetime import date, time
import sqlite3
import os
from app.config import Config
from app.models import db, Kurs, Seminar

def setup_database(app):
    # in case we are running the app for the first time, 
    # we need to create the database file and fill it with test data
    db_path = Config.BASEDIR + "/../instance/database.db"
    need_new_database = not os.path.exists(db_path)
    if need_new_database:
        print("Creating database file at", db_path)
        with sqlite3.connect(db_path):
            pass

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Erstellt ALLE Tabellen aus models.py

        if need_new_database:
            populate_database()



def populate_database():
    # Erstellen Sie die Tabellen in der Datenbank
    #db.create_all()

    # Beispielhafte Daten für Kurse
    kurse_data = [
        ('Python Grundlagen', 2, 40, 'Skript001', 1),
        ('Flask Webentwicklung', 3, 50, 'Skript002', 2),
        ('Datenanalyse mit Pandas', 2, 45, 'Skript003', 3),
        ('Maschinelles Lernen mit scikit-learn', 4, 60, 'Skript004', 4),
        ('Datenbanken mit SQLAlchemy', 2, 55, 'Skript005', 5)
    ]

    # Beispielhafte Daten für Seminare
    seminare_data = [
        ('2025-04-01', '09:00:00', 'Musterstraße 1', '1', '1010', 'Python Grundlagen'),
        ('2025-04-02', '14:00:00', 'Beispielweg 2', '2', '1020', 'Python Grundlagen'),
        ('2025-04-03', '10:00:00', 'Programmgasse 3', '3', '1030', 'Python Grundlagen'),
        ('2025-04-04', '15:00:00', 'Codeallee 4', '4', '1040', 'Python Grundlagen'),
        ('2025-04-05', '11:00:00', 'Devstraße 5', '5', '1050', 'Python Grundlagen'),
        ('2025-04-06', '09:00:00', 'Flaskweg 6', '6', '1060', 'Flask Webentwicklung'),
        ('2025-04-07', '14:00:00', 'Webstraße 7', '7', '1070', 'Flask Webentwicklung'),
        ('2025-04-08', '10:00:00', 'Appgasse 8', '8', '1080', 'Flask Webentwicklung'),
        ('2025-04-09', '15:00:00', 'Devgasse 9', '9', '1090', 'Flask Webentwicklung'),
        ('2025-04-10', '11:00:00', 'Codegasse 10', '10', '1100', 'Flask Webentwicklung'),
        ('2025-04-11', '09:00:00', 'Datengasse 11', '11', '1110', 'Datenanalyse mit Pandas'),
        ('2025-04-12', '14:00:00', 'Analysegasse 12', '12', '1120', 'Datenanalyse mit Pandas'),
        ('2025-04-13', '10:00:00', 'Pandasweg 13', '13', '1130', 'Datenanalyse mit Pandas'),
        ('2025-04-14', '15:00:00', 'Sciweg 14', '14', '1140', 'Datenanalyse mit Pandas'),
        ('2025-04-15', '11:00:00', 'MLstraße 15', '15', '1150', 'Datenanalyse mit Pandas'),
        ('2025-04-16', '09:00:00', 'MLGasse 16', '16', '1160', 'Maschinelles Lernen mit scikit-learn'),
        ('2025-04-17', '14:00:00', 'Scikitweg 17', '17', '1170', 'Maschinelles Lernen mit scikit-learn'),
        ('2025-04-18', '10:00:00', 'AIstraße 18', '18', '1180', 'Maschinelles Lernen mit scikit-learn'),
        ('2025-04-19', '15:00:00', 'Dataweg 19', '19', '1190', 'Maschinelles Lernen mit scikit-learn'),
        ('2025-04-20', '11:00:00', 'MLGasse 20', '20', '1200', 'Maschinelles Lernen mit scikit-learn'),
        ('2025-04-21', '09:00:00', 'DBweg 21', '21', '1210', 'Datenbanken mit SQLAlchemy'),
        ('2025-04-22', '14:00:00', 'SQLGasse 22', '22', '1220', 'Datenbanken mit SQLAlchemy'),
        ('2025-04-23', '10:00:00', 'Alchemyweg 23', '23', '1230', 'Datenbanken mit SQLAlchemy'),
        ('2025-04-24', '15:00:00', 'Tabellenstraße 24', '24', '1240', 'Datenbanken mit SQLAlchemy'),
        ('2025-04-25', '11:00:00', 'Modelgasse 25', '25', '1250', 'Datenbanken mit SQLAlchemy')
    ]

    # Fügen Sie die Kurse zur Datenbank hinzu
    for kurs_data in kurse_data:
        kurs = Kurs(
            kursname=kurs_data[0],
            anzahl_organisatoren=kurs_data[1],
            vorbereitungsdauer=kurs_data[2],
            skriptentyp_nr=kurs_data[3],
            autoren_nr=kurs_data[4]
        )
        db.session.add(kurs)

    # Fügen Sie die Seminare zur Datenbank hinzu
    for seminar_data in seminare_data:
        seminar = Seminar(
            datum=date.fromisoformat(seminar_data[0]),
            uhrzeit=time.fromisoformat(seminar_data[1]),
            strasse=seminar_data[2],
            hausnr=seminar_data[3],
            plz=seminar_data[4],
            kursname=seminar_data[5]
        )
        db.session.add(seminar)

    # Speichern Sie die Änderungen in der Datenbank
    db.session.commit()
    print("Datenbank erfolgreich mit Kursen und Seminaren befüllt.")
