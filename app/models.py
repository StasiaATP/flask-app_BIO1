from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime

# Datenbank-Objekt für SQLAlchemy erstellen
db = SQLAlchemy()


# -------------------------------------------------------------------
# Modell für Benutzer (User)
# - Speichert Login-Daten und ist mit Person verknüpft
# -------------------------------------------------------------------
class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Für die Beziehungen zu abgeleiteten Klassen (Person, Angestellte, etc.)
    type = Column(String, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
    }


# -------------------------------------------------------------------
# Modell für Personendaten (Basisklasse für Teilnehmer, Angestellte, etc.)
# - Enthält persönliche Infos wie Name & Adresse
# -------------------------------------------------------------------
class Person(User):
    id = Column(Integer, ForeignKey("user.id"))
    sozial_vers_nr = Column(String, primary_key=True)
    vorname = Column(String, nullable=False)
    nachname = Column(String, nullable=False)
    plz = Column(String, nullable=False)
    ort = Column(String, nullable=False)
    strasse = Column(String, nullable=False)
    hausnr = Column(String, nullable=False)
    telefonnummer = Column(String)

    __mapper_args__ = {"polymorphic_identity": "person"}


# -------------------------------------------------------------------
# Teilnehmer (Kunde) - Erbt von Person
# -------------------------------------------------------------------
class Teilnehmer(Person):
    sozial_vers_nr = Column(Integer, ForeignKey("person.sozial_vers_nr"))
    kunden_nr = Column(Integer, primary_key=True)
    bevorzugter_ausbilder = Column(String, ForeignKey("ausbilder.kennzeichnung"))

    reservierungen = db.relationship("Reserviert", back_populates="teilnehmer", uselist=False)

    __mapper_args__ = {"polymorphic_identity": "teilnehmer"}


# -------------------------------------------------------------------
# Angestellte - Erbt von Person
# -------------------------------------------------------------------
class Angestellte(Person):
    sozial_vers_nr = Column(Integer, ForeignKey("person.sozial_vers_nr"))
    angestellten_nr = Column(Integer, primary_key=True)
    konto_nr = Column(String)
    kontostand = Column(Integer)  # in cent

    entlehnte_skripte = db.relationship("SkriptExemplar", back_populates="entlehnt_von")

    __mapper_args__ = {"polymorphic_identity": "angestellte"}


# -------------------------------------------------------------------
# Ausbilder - Erbt von Angestellte
# -------------------------------------------------------------------
class Ausbilder(Angestellte):
    angestellten_nr = Column(Integer, ForeignKey("angestellte.angestellten_nr"), nullable=False)
    kennzeichnung = Column(String, primary_key=True)
    datum_einstellung = Column(Date)

    seminar_abhaltungen = db.relationship("BildetAus", back_populates="ausbilder")

    __mapper_args__ = {"polymorphic_identity": "ausbilder"}


# -------------------------------------------------------------------
# Organisator - Erbt von Angestellte
# -------------------------------------------------------------------
class Organisator(Angestellte):
    angestellten_nr = Column(Integer, ForeignKey("angestellte.angestellten_nr"), nullable=False, primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "organisator"}


# -------------------------------------------------------------------
# Kurs
# -------------------------------------------------------------------
class Kurs(db.Model):
    kursname = Column(String, primary_key=True)
    anzahl_organisatoren = Column(Integer)
    vorbereitungsdauer = Column(Integer)
    skriptentyp_nr = Column(Integer)
    autor = Column(String)

    seminare = db.relationship("Seminar", back_populates="kurs")


# -------------------------------------------------------------------
# Seminar
# -------------------------------------------------------------------
class Seminar(db.Model):
    id = Column(Integer, primary_key=True)
    datum_uhrzeit = Column(DateTime, nullable=False)
    strasse = Column(String, nullable=False)
    hausnr = Column(String, nullable=False)
    plz = Column(String, nullable=False)
    kursname = Column(String, ForeignKey("kurs.kursname"), nullable=False)

    kurs = db.relationship("Kurs", back_populates="seminare")
    reservierungen = db.relationship("Reserviert", back_populates="seminar")
    abhaltungen = db.relationship("BildetAus", back_populates="seminar")

    # Datum und Uhrzeit werden als DateTime-Objekt kombiniert gespeichert
    # Damit man auf beides einzeln zugreifen kann, werden properties definiert
    @property
    def datum(self):
        return self.datum_uhrzeit.date()

    @property
    def uhrzeit(self):
        return self.datum_uhrzeit.time()
    
    @property
    def ausbilder(self):
        """Erstellt eine Liste aller Ausbilder (nur username) für die Adminseite"""
        result = []
        for abhaltung in self.abhaltungen:
            result.append(abhaltung.ausbilder.username)
        return ", ".join(result)


# -------------------------------------------------------------------
# Skript-Exemplar
# -------------------------------------------------------------------
class SkriptExemplar(db.Model):
    inventar_nr = Column(Integer, primary_key=True)
    kursname = Column(String, ForeignKey("kurs.kursname"), nullable=False)

    entlehnt_von_nr = Column(Integer, ForeignKey("angestellte.angestellten_nr"))
    entlehnt_von = db.relationship(
        "Angestellte", back_populates="entlehnte_skripte", uselist=False
    )


# -------------------------------------------------------------------
# HatAversion (Ausbilder mag andere nicht)
# -------------------------------------------------------------------
class HatAversion(db.Model):
    kennzeichnung_ausbilder_1 = Column(
        String, ForeignKey("ausbilder.kennzeichnung"), primary_key=True
    )
    kennzeichnung_ausbilder_2 = Column(
        String, ForeignKey("ausbilder.kennzeichnung"), primary_key=True
    )

    ausbilder_1 = db.relationship("Ausbilder", foreign_keys=[kennzeichnung_ausbilder_1])
    ausbilder_2 = db.relationship("Ausbilder", foreign_keys=[kennzeichnung_ausbilder_2])


# -------------------------------------------------------------------
# KannAbhalten Welcher Ausbilder kann welchen Kurs in welcher Sprache abhalten 
# (3-stellige Kurs-Ausbilder-Sprache-Verknüpfung)
# -------------------------------------------------------------------
class KannAbhalten(db.Model):
    ausbilder_kennzeichnung = Column(
        String, ForeignKey("ausbilder.kennzeichnung"), primary_key=True
    )
    kursname = Column(String, ForeignKey("kurs.kursname"), primary_key=True)
    sprache = Column(String, primary_key=True)

    ausbilder = db.relationship("Ausbilder")
    kurs = db.relationship("Kurs")


# -------------------------------------------------------------------
# BildetAus (Welcher Ausbilder hält welches Seminar)
# -------------------------------------------------------------------
class BildetAus(db.Model):
    seminar_id = Column(Integer, ForeignKey("seminar.id"), primary_key=True)
    ausbilder_kennzeichnung = Column(
        String, ForeignKey("ausbilder.kennzeichnung"), primary_key=True
    )

    seminar = db.relationship("Seminar", back_populates="abhaltungen")
    ausbilder = db.relationship("Ausbilder", back_populates="seminar_abhaltungen")


# -------------------------------------------------------------------
# Reserviert (Teilnehmer bucht ein Seminar)
# -------------------------------------------------------------------
class Reserviert(db.Model):
    reservierungsnummer = Column(Integer, primary_key=True)
    kunden_nr = Column(Integer, ForeignKey("teilnehmer.kunden_nr"), nullable=False)
    seminar_id = Column(Integer, ForeignKey("seminar.id"), nullable=False)

    teilnehmer = db.relationship("Teilnehmer", back_populates="reservierungen")
    seminar = db.relationship("Seminar", back_populates="reservierungen")
