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

from datetime import date, datetime
import sqlite3
import os
from werkzeug.security import generate_password_hash
from app.config import Config
from app.models import *

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
    """Fülle die Datenbank mit Beispieldaten zum Testen"""

    # Teilnehmer:
    # username, password, sozial_vers_nr, vorname, nachname, plz, ort, strasse, hausnr
    teilnehmer_data = [
            ( "test", "test", 1, "Test", "User", 1000, "Wien", "Teststrasse", 1),
            ( "teilnehmer", "abc", 2, "Max", "Mustermann", 1000, "Wien", "Musterstraße", 9),
    ]

    for data in teilnehmer_data:
        teilnehmer = Teilnehmer(
            username=data[0], 
            password=generate_password_hash(data[1]), 
            sozial_vers_nr=data[2],
            vorname=data[3],
            nachname=data[4],
            plz=data[5],
            ort=data[6],
            strasse=data[7],
            hausnr=data[8]
        )
        db.session.add(teilnehmer)


    # Ausbilder:
    # username, password, sozial_vers_nr, vorname, nachname, plz, ort, strasse, hausnr, kennzeichnung, konto_nr, kontostand, datum_einstellung
    ausbilder_data = [
            ( "hans", "abc", 10, "Hans", "Mayer", 1010, "Wien", "Am Graben", 5, "AT123456789", 1000, date(2025, 1, 1)),
            ( "maria", "abc", 11, "Maria", "Schmid", 1090, "Wien", "Weg", 12, "AT99977742", 0, date(2024, 10, 1)),
            ( "gerold", "abc", 12, "Gerold", "Mauer", 1190, "Wien", "Gasse", 8, "AT88877848", 10000, date(2022, 10, 1)),
            ]

    for data in ausbilder_data:
        ausbilder = Ausbilder(
            username=data[0], 
            password=generate_password_hash(data[1]), 
            sozial_vers_nr=data[2],
            vorname=data[3],
            nachname=data[4],
            plz=data[5],
            ort=data[6],
            strasse=data[7],
            hausnr=data[8],
            kennzeichnung=data[0], 
            konto_nr=data[9],
            kontostand=data[10],
            datum_einstellung=data[11],
        )
        db.session.add(ausbilder)

    # Organisator:
    # username, password, sozial_vers_nr, vorname, nachname, plz, ort, strasse, hausnr
    organisator_data = [
            ( "org", "abc", 20, "Peter", "Huber", 1030, "Wien", "Die Straße", 3),
            ]

    for data in organisator_data:
        organisator = Organisator(
            username=data[0], 
            password=generate_password_hash(data[1]), 
            sozial_vers_nr=data[2],
            vorname=data[3],
            nachname=data[4],
            plz=data[5],
            ort=data[6],
            strasse=data[7],
            hausnr=data[8],
        )
        db.session.add(organisator)

    # Kurse:
    # kursname, anzahl_organisatoren, vorbereitungsdauer, skriptentyp_nr, autor
    kurse_data = [
        ('Python Grundlagen', 2, 40, 1, "Hans Mayer"),
        ('Flask Webentwicklung', 3, 50, 2, "Maria Huber"),
        ('Datenanalyse mit Pandas', 2, 45, 3, "Peter Müller"),
        ('Maschinelles Lernen mit scikit-learn', 4, 60, 4, "Anna Wagner"),
        ('Datenbanken mit SQLAlchemy', 2, 55, 5, "Maria Huber")
    ]

    # Fügen Sie die Kurse zur Datenbank hinzu
    for kurs_data in kurse_data:
        kurs = Kurs(
            kursname=kurs_data[0],
            anzahl_organisatoren=kurs_data[1],
            vorbereitungsdauer=kurs_data[2],
            skriptentyp_nr=kurs_data[3],
            autor=kurs_data[4]
        )
        db.session.add(kurs)

    # Seminare:
    # datum, uhrzeit, strasse, hausnr, plz, kursname
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

    # Fügen Sie die Seminare zur Datenbank hinzu
    for seminar_data in seminare_data:
        seminar = Seminar(
            datum_uhrzeit=datetime.fromisoformat(seminar_data[0] + ' ' + seminar_data[1]),
            strasse=seminar_data[2],
            hausnr=seminar_data[3],
            plz=seminar_data[4],
            kursname=seminar_data[5]
        )
        db.session.add(seminar)

    # Reservierungen:
    reserviert_data = [
            (1, 1), # erster user reserviert ersten kurs
            (1, 7),
            (1, 17),
    ]

    for data in reserviert_data:
        reservierung = Reserviert(
            kunden_nr=data[0],
            seminar_id=data[1]
        )
        db.session.add(reservierung)

    # BildetAus (wer hält welchen Kurs ab):
    bildet_aus_data = [
            (1, "hans"),
            (2, "hans"),
            (2, "maria"),
            (3, "maria"),
            (4, "maria"),
            (5, "maria"),
    ]

    for data in bildet_aus_data:
        ausbildung = BildetAus(
            seminar_id=data[0],
            ausbilder_kennzeichnung=data[1],
        )
        db.session.add(ausbildung)

    # KannAbhalten (welcher Ausbilder kann welchen Kurs in welcher Sprache abhalten)
    kann_abhalten_data = [
            ("hans", "Python Grundlagen", "Deutsch"),
            ("hans", "Python Grundlagen", "Englisch"),
            ("maria", "Python Grundlagen", "Englisch"),
            ("maria", "Flask Webentwicklung", "Deutsch"),
            ("maria", "Datenanalyse mit Pandas", "Englisch"),
            ("maria", "Maschinelles Lernen mit scikit-learn", "Deutsch"),
            ("maria", "Datenbanken mit SQLAlchemy", "Englisch"),
            ("maria", "Datenbanken mit SQLAlchemy", "Klingonisch"),
            ("gerold", "Flask Webentwicklung", "Esperanto"),
    ]

    for data in kann_abhalten_data:
        abhaltung = KannAbhalten(
            ausbilder_kennzeichnung=data[0],
            kursname=data[1],
            sprache=data[2]
        )
        db.session.add(abhaltung)

    # HatAversion (Ausbilder mag anderen Ausbilder nicht)
    aversion_data = [
            ("hans", "gerold"), # hans mag gerold nicht
    ]
    for data in aversion_data:
        aversion = HatAversion(
            kennzeichnung_ausbilder_1=data[0],
            kennzeichnung_ausbilder_2=data[1]
        )
        db.session.add(aversion)

    # Erzeuge pro Kurs 10 Skriptexemplare
    for kurs in kurse_data:
        for i in range(10):
            skript = SkriptExemplar(
                kursname=kurs[0],
                entlehnt_von_nr=None
            )
            if i == 0:
                # der erste user hat jeweils das erste Skript entlehnt
                skript.entlehnt_von_nr = 1

            db.session.add(skript)

    # Führe alle obigen Aktionen aus und speichere die Änderungen in der Datenbank
    db.session.commit()
    print("Datenbank erfolgreich mit Kursen und Seminaren befüllt.")
