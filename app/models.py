from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Datenbank-Objekt für SQLAlchemy erstellen
db = SQLAlchemy()

# -------------------------------------------------------------------
# Modell für Benutzer (User)
# - Speichert Login-Daten und ist mit Person verknüpft
# -------------------------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(150), unique=True, nullable=False)  
    password = db.Column(db.String(150), nullable=False)  
    sozial_vers_nr = db.Column(db.String(15), db.ForeignKey('person.sozial_vers_nr'), nullable=False)

    person = db.relationship('Person', back_populates="user")

# -------------------------------------------------------------------
# Modell für Personendaten
# - Enthält persönliche Infos wie Name & Adresse
# - Wird mit User, Teilnehmer & Angestellter verknüpft
# -------------------------------------------------------------------
class Person(db.Model):
    sozial_vers_nr = db.Column(db.String(15), primary_key=True)
    vorname = db.Column(db.String(100), nullable=False)  
    nachname = db.Column(db.String(100), nullable=False)  
    plz = db.Column(db.String(5), nullable=False)  
    ort = db.Column(db.String(100), nullable=False)  
    strasse = db.Column(db.String(100), nullable=False)  
    hausnr = db.Column(db.String(10), nullable=False)  

    user = db.relationship('User', uselist=False, back_populates="person")
    teilnehmer = db.relationship('Teilnehmer', backref='person_teilnehmer', uselist=False)
    angestellte = db.relationship('Angestellte', backref='person_angestellte', uselist=False)

# -------------------------------------------------------------------
# Telefonnummer (Optional)
# -------------------------------------------------------------------
class Telefonnummer(db.Model):
    telefon_nr = db.Column(db.String(15), primary_key=True)  
    sozial_vers_nr = db.Column(db.String(15), db.ForeignKey('person.sozial_vers_nr'), nullable=False)  

    person = db.relationship('Person', backref='telefonnummer', uselist=False)

# -------------------------------------------------------------------
# Teilnehmer (Kunde)
# -------------------------------------------------------------------
class Teilnehmer(db.Model):
    kunden_nr = db.Column(db.Integer, primary_key=True)  
    sozial_vers_nr = db.Column(db.String(15), db.ForeignKey('person.sozial_vers_nr'), nullable=False)
    kennzeichnung = db.Column(db.String(50))  

# -------------------------------------------------------------------
# Angestellte
# -------------------------------------------------------------------
class Angestellte(db.Model):
    angestellten_nr = db.Column(db.Integer, primary_key=True)
    sozial_vers_nr = db.Column(db.String(15), db.ForeignKey('person.sozial_vers_nr'), nullable=False)
    konto_nr = db.Column(db.String(20))  
    kontostand = db.Column(db.Float)  

# -------------------------------------------------------------------
# Ausbilder
# -------------------------------------------------------------------
class Ausbilder(db.Model):
    kennzeichnung = db.Column(db.String(50), primary_key=True)
    datum_einstellung = db.Column(db.Date)  
    angestellten_nr = db.Column(db.Integer, db.ForeignKey('angestellte.angestellten_nr'))  

# -------------------------------------------------------------------
# Organisator
# -------------------------------------------------------------------
class Organisator(db.Model):
    organisator_nr = db.Column(db.Integer, primary_key=True)  
    angestellten_nr = db.Column(db.Integer, db.ForeignKey('angestellte.angestellten_nr'))  

# -------------------------------------------------------------------
# Kurs
# -------------------------------------------------------------------
class Kurs(db.Model):
    kursname = db.Column(db.String(100), primary_key=True)
    anzahl_organisatoren = db.Column(db.Integer)  
    vorbereitungsdauer = db.Column(db.Integer)  
    skriptentyp_nr = db.Column(db.String(50))  
    autoren_nr = db.Column(db.Integer, db.ForeignKey('autor.autoren_nr'))  

# -------------------------------------------------------------------
# Sprache
# -------------------------------------------------------------------
class Sprache(db.Model):
    bezeichnung = db.Column(db.String(100), primary_key=True)

# -------------------------------------------------------------------
# Seminar
# -------------------------------------------------------------------
class Seminar(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    datum = db.Column(db.Date, nullable=False)  
    uhrzeit = db.Column(db.Time, nullable=False)  
    strasse = db.Column(db.String(100), nullable=False)  
    hausnr = db.Column(db.String(10), nullable=False)  
    plz = db.Column(db.String(5), nullable=False)  
    kursname = db.Column(db.String(100), db.ForeignKey('kurs.kursname'), nullable=False)

# -------------------------------------------------------------------
# Autor
# -------------------------------------------------------------------
class Autor(db.Model):
    autoren_nr = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  

# -------------------------------------------------------------------
# Skript-Exemplar
# -------------------------------------------------------------------
class SkriptExemplar(db.Model):
    inventar_nr = db.Column(db.Integer, primary_key=True)  
    kursname = db.Column(db.String(100), db.ForeignKey('kurs.kursname'), nullable=False)  

# -------------------------------------------------------------------
# HatAversion (Ausbilder mag andere nicht)
# -------------------------------------------------------------------
class HatAversion(db.Model):
    ausbilder_1 = db.Column(db.String(50), db.ForeignKey('ausbilder.kennzeichnung'), primary_key=True)  
    ausbilder_2 = db.Column(db.String(50), db.ForeignKey('ausbilder.kennzeichnung'), primary_key=True)  

# -------------------------------------------------------------------
# HaeltAbIn (Kurs-Sprache-Verknüpfung)
# -------------------------------------------------------------------
class HaeltAbIn(db.Model):
    kennzeichnung = db.Column(db.String(50), db.ForeignKey('ausbilder.kennzeichnung'), primary_key=True)  
    kursname = db.Column(db.String(100), db.ForeignKey('kurs.kursname'), primary_key=True)  
    bezeichnung = db.Column(db.String(100), db.ForeignKey('sprache.bezeichnung'), primary_key=True)  

# -------------------------------------------------------------------
# BildetAus (Welcher Ausbilder hält welches Seminar)
# -------------------------------------------------------------------
class BildetAus(db.Model):
    datum = db.Column(db.Date, primary_key=True)  
    uhrzeit = db.Column(db.Time, primary_key=True)  
    kennzeichnung = db.Column(db.String(50), db.ForeignKey('ausbilder.kennzeichnung'))  

# -------------------------------------------------------------------
# Reserviert (Teilnehmer bucht ein Seminar)
# -------------------------------------------------------------------
class Reserviert(db.Model):
    reservierungsnummer = db.Column(db.Integer, primary_key=True)  
    kunden_nr = db.Column(db.Integer, db.ForeignKey('teilnehmer.kunden_nr'), nullable=False)  
    datum = db.Column(db.Date, nullable=False)  
    uhrzeit = db.Column(db.Time, nullable=False)  

# -------------------------------------------------------------------
# Entlehnt (Angestellte leihen Skripte aus)
# -------------------------------------------------------------------
class Entlehnt(db.Model):
    angestellten_nr = db.Column(db.Integer, db.ForeignKey('angestellte.angestellten_nr'), primary_key=True)  
    inventar_nr = db.Column(db.Integer, db.ForeignKey('skript_exemplar.inventar_nr'), primary_key=True)  
