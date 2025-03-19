"""
common_routes.py – Enthält alle gemeinsamen Routes (Webseiten)
--------------------------------------------------------
Dieses Modul definiert alle gemeinsamen API-Endpunkte der Webanwendung, 
einschließlich Login, Registrierung und Benutzerdatenverwaltung
"""

from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import db, User, Teilnehmer, Ausbilder

# Blueprint für die Routen erstellen
common_routes = Blueprint('routes', __name__) # Das muss routes heißen, ansonsten funktioniert flask_login.logout_user nicht

# -----------------------------------
# Funktion zur Initialisierung des Login-Managers
# -----------------------------------
@login_required
def load_user(user_id):
    return User.query.get(int(user_id))
# -----------------------------------
# Home Route
# -----------------------------------
@common_routes.route('/')
def index():
    return render_template('index.html')

# -----------------------------------
# Login Route
# -----------------------------------
@common_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    return render_template('login.html')

# -----------------------------------
# Registrierung eines Teilnehmers
# -----------------------------------
@common_routes.route('/register', methods=['GET', 'POST'])
def register():
    ausbilder_liste = Ausbilder.query.all()  # Alle Ausbilder holen

    if request.method == 'POST':
        # Daten aus dem Formular
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        # Personendaten
        sozial_vers_nr = request.form['sozial_vers_nr']
        vorname = request.form['vorname']
        nachname = request.form['nachname']
        plz = request.form['plz']
        ort = request.form['ort']
        strasse = request.form['strasse']
        hausnr = request.form['hausnr']
        telefonnummer = request.form['telefonnummer']
        bevorzugter_ausbilder = request.form.get('bevorzugter_ausbilder', None)


        # Teilnehmer speichern
        teilnehmer = Teilnehmer(
                username=username,
                password=password,
                sozial_vers_nr=sozial_vers_nr,
                vorname=vorname,
                nachname=nachname,
                plz=plz,
                ort=ort,
                strasse=strasse,
                hausnr=hausnr,
                telefonnummer=telefonnummer,
                bevorzugter_ausbilder=bevorzugter_ausbilder
        )
        db.session.add(teilnehmer)
        db.session.commit()

        return redirect('/login')
    return render_template('register.html', ausbilder_liste=ausbilder_liste)

# -----------------------------------
# Benutzerprofil bearbeiten
# -----------------------------------
@common_routes.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    ausbilder_liste = Ausbilder.query.all()
    
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.vorname = request.form['vorname']
        current_user.nachname = request.form['nachname']
        current_user.plz = request.form['plz']
        current_user.ort = request.form['ort']
        current_user.strasse = request.form['strasse']
        current_user.hausnr = request.form['hausnr']
        current_user.telefonnummer = request.form['telefonnummer']
        current_user.bevorzugter_ausbilder = request.form.get('bevorzugter_ausbilder', None)


        db.session.commit()
        return redirect('/edit') # bleibe auf der edit Seite um Änderungen zu sehen
    return render_template('edit_user.html', ausbilder_liste=ausbilder_liste)
    
# -----------------------------------
# Logout Route
# -----------------------------------
@common_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
