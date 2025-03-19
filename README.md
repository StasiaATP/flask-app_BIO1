<center>

# **DEVTRACK - Seminarverwaltungssystem**

</center>



**Projektbeschreibung**

*DEVTRACK ist eine Plattform zur effizienten Verwaltung und Buchung von Seminaren. Teilnehmer können sich registrieren, Seminare buchen und ihre Daten verwalten, während Ausbilder ihre Seminare organisieren und verwalten können. Organisatoren überwachen das gesamte Seminarangebot und können die Planung optimieren.*


**Tech-Stack**

*Unser Projekt basiert auf folgenden Technologien:*

- Python & Flask – Backend-Entwicklung

- HTML, CSS (modal.css), Bootstrap – Frontend-Design

- SQLAlchemy – Datenbank-ORM

- SQLite – Datenbank

- GitHub – Versionierung & Zusammenarbeit


### Verwendete Python-Bibliotheken (requirements.txt)

```plaintext
alembic==1.15.1
blinker==1.9.0
click==8.1.8
dnspython==2.7.0
email_validator==2.2.0
Flask==3.1.0
Flask-Login==0.6.3
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.2
greenlet==3.1.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
Mako==1.3.9
MarkupSafe==3.0.2
SQLAlchemy==2.0.39
typing_extensions==4.12.2
Werkzeug==3.1.3
WTForms==3.2.1
```

### Projektstruktur in VS Code

```plaintext
flask-app_BIO1/
│── app/
│   │── __init__.py
│   │── config.py
│   │── db_setup.py
│   │── models.py
│   │── teilnehmer_routes.py
│   │── ausbilder_routes.py
│── instance/
│── static/
│   │── modal.css
│   │── devtrack_logo.png
│   │── programming.png
│── templates/
│   │── base.html
│   │── index.html
│   │── login.html
│   │── register.html
│   │── edit_user.html
│   │── reserve.html
│   │── reservierungen.html
│   │── seminar_details.html
│   │── ausbilder_seminare.html
│── requirements.txt
│── README.md
```

## 1. Erste Schritte: Installation & Setup

### 1.1 Klone das Repository:
```bash
git clone https://github.com/StasiaATP/flask-app_BIO1
cd flask-app_BIO1/
```
### 1.2 Erstelle eine virtuelle Umgebung und installiere Abhängigkeiten:
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```
### 1.3 Datenbank initialisieren:
```bash
python app/db_setup.py
```
### 1.4 Starte die Anwendung:
```bash
flask run
```
Die Anwendung läuft nun unter http://127.0.0.1:5000/.


**2. Funktionalitäten**

*2.1 Teilnehmer-Funktionen:*

- Seminare anzeigen (Kursname, Datum, Uhrzeit, Ort)

- Reservierungen vornehmen/stornieren

- Bevorzugte Ausbilder speichern

- Eigene Benutzerdaten verwalten

- Liste der Reservierungen einsehen

- Login & Logout


*2.2 Ausbilder-Funktionen:*

- Eigene Seminare anzeigen

- Teilnehmerlisten einsehen

- Neue Seminare erstellen, bearbeiten oder löschen

- Login & Logout
  

*2.3 Organisator-Funktionen:*

- Alle Seminare verwalten

- Ausbilder zuweisen

- Teilnehmerzahlen überwachen

- Kursorte & Zeitpläne verwalten

- Login & Logout


*2.4 Admin-Funktionen:*


**3. Team & Aufgaben**

| Teammitglieder               | Aufgabe                                      |
|------------------------------|---------------------------------------------|
| **Anastasia Ceta & Sabina Raykova** | Teilnehmer-Dashboard, Login/Register, CSS Styling, Datenverwaltung |
| **Edit Felföldi**            | Ausbilder-Dashboard, eigene Routes, HTML für Ausbilder, Seminarverwaltung |
| **Nicholas Wedige**          | Organisator-Dashboard, Kursverwaltung, Teilnehmerzahl-Überwachung |
| **Doris Steinbauer**         | Datenbankstruktur (models.py), Fehlerbeseitigung, Admin-Dashboard |


**4. 🚀 Lessons Learned & Fazit**

„Mit großem Code kommt großes Debugging“ – ein Projekt über Flask, SQLAlchemy & die Kunst, nicht den Verstand zu verlieren.

*Herausforderungen & Schwierigkeiten*

4.1 Projektstruktur & Rollen
Die Aufteilung in verschiedene Masken für Teilnehmer, Ausbilder, Organisatoren und Admin erforderte eine saubere Routenverwaltung. Flask-Blueprints waren die Rettung, aber die Organisation der Datenbankrelationen (SQLite & SQLAlchemy) war eine Herausforderung – besonders beim Mapping zwischen Teilnehmern, Seminaren und Reservierungen.

4.2 CSS war unser "Endgegner"
Ein einfaches Formular stylen? Kein Problem. Aber eine komplette Anwendung mit mehreren Benutzerrollen, Responsive Design und einer sich ständig ändernden Struktur? CSS-Chaos war vorprogrammiert. Positionierungsprobleme, zerschossene Layouts, überlagerte Dropdowns – wir haben alles gesehen.

4.3 "GitHub-Kriege": Merge-Konflikte & Versionierung
Mit fünf Personen gleichzeitig an einem Projekt zu arbeiten, war nicht ohne. Pull-Requests, Merge-Konflikte und das ständige Managen von unser einziger main - Branch haben uns gezwungen, besser zu kommunizieren und sauber zu dokumentieren.

4.4 Flask-Login & Authentifizierung
Die Implementierung der Login-Logik war schwieriger als erwartet. Besonders tricky:
- Sicherstellen, dass nach dem Login die richtige Maske (Teilnehmer, Ausbilder, Organisator) geladen wird.
- Session-Handling korrekt umsetzen, ohne dass man nach jedem Login plötzlich auf der Startseite landet.
- Zugriffsbeschränkungen richtig setzen (z. B. sollte ein Teilnehmer nicht plötzlich Organisator-Funktionen sehen).


**5. Was wir verbessern könnten & zukünftige Erweiterungen**

5.1 Zusätzliche Funktionalitäten (basierend auf dem REL-Schema) - wir haben eine solide Basis geschaffen, aber das System könnte noch smarter werden. 

Beispiele:

    - Skriptenverwaltung → Teilnehmer könnten sich Kursmaterialien ausleihen (Relation ENTLEHNT);
    - Mehrsprachigkeit der Seminare → Jeder Kurs könnte in mehreren Sprachen angeboten werden (Relation HÄLT_AB_IN);
    - Automatische Benachrichtigungen → Teilnehmer erhalten eine E-Mail, wenn sich ihr Seminar ändert;
    - Maximale Teilnehmerzahl pro Seminar → Reservierungen verhindern, wenn Kurs voll ist;
    - Bevorzugte Ausbilder mit Bewertungen → Teilnehmer könnten ihre Favoriten markieren oder eine z.B Sternebewertung abgeben ...


5.2 Bessere Planung des CSS-Designs von Anfang an:
Eine frühere Absprache zum Layout und Design hätte uns später viel Zeit gespart. Vorschlag für die Zukunft: Design-Vorlagen vorab skizzieren und die CSS-Dateien strukturierter aufteilen.

5.3 Mehr Tests zur Fehlererkennung:
Unit-Tests für Flask-Routes, Datenbankabfragen und die Authentifizierung hätten geholfen, viele Fehler früh zu entdecken. Ein Ziel für die Zukunft: automatisierte Tests.

5.4 Bessere Dokumentation & Readme-Updates:
Während der Entwicklung hätten wir uns mehr auf detaillierte Code-Kommentare und eine Entwickler-Dokumentation konzentrieren können. So kann man schneller den Projekt-Überblick bekommen.


Danke fürs Durchlesen!

Falls du Fragen hast oder dieses Projekt erweitern möchtest, erstelle einfach ein Issue oder einen Pull Request. Viel Spaß beim Entwickeln!

**Happy Coding!**


## Test Zugangsdaten für die App:

| Benutzername | Passwort | Typ         |
| ------------ | -------- | ----------- |
| test         | test     | Teilnehmer  |
| teilnehmer   | abc      | Teilnehmer  |
| hans         | abc      | Ausbilder   |
| maria        | abc      | Ausbilder   |
| gerold       | abc      | Ausbilder   |
| org          | abc      | Organisator |
