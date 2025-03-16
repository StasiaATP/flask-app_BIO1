"""
routes.py – Enthält alle Routen der Flask-App
--------------------------------------------------------
Dieses Modul definiert alle API-Endpunkte der Webanwendung, 
einschließlich Login, Registrierung und Seminarverwaltung.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db, User, Teilnehmer, Seminar, Reserviert

# Blueprint für die Routen erstellen
routes = Blueprint('routes', __name__)

# -----------------------------------
# Funktion zur Initialisierung des Login-Managers
# -----------------------------------
@login_required
def load_user(user_id):
    return User.query.get(int(user_id))

# -----------------------------------
# Home Route
# -----------------------------------
@routes.route('/')
def index():
    return render_template('index.html')

# -----------------------------------
# Login Route
# -----------------------------------
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('routes.index'))
    return render_template('login.html')

# -----------------------------------
# Registrierung eines Teilnehmers
# -----------------------------------
@routes.route('/register', methods=['GET', 'POST'])
def register():
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
                hausnr=hausnr
        )
        db.session.add(teilnehmer)
        db.session.commit()

        return redirect(url_for('routes.login'))
    return render_template('register.html')

# -----------------------------------
# Reservierung eines Seminars
# -----------------------------------
@routes.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    if request.method == 'POST':
        seminar_id = request.form.get('seminar')
        if seminar_id:
            seminar = Seminar.query.get(seminar_id)
            if seminar:
                new_reservation = Reserviert(
                    seminar_id=seminar_id,
                    kunden_nr=current_user.id,
                )
                db.session.add(new_reservation)
                db.session.commit()
                return redirect(url_for('routes.index'))
    seminars = Seminar.query.all()
    return render_template('reserve.html', seminars=seminars)

# -----------------------------------
# Liste der Reservierungen anzeigen
# -----------------------------------
@routes.route('/reservierungen')
@login_required
def reservierungen():
    user_reservations = Reserviert.query.filter_by(kunden_nr=current_user.id).all()
    return render_template('reservierungen.html', reservations=user_reservations)

# -----------------------------------
# Stornieren einer Reservierung
# -----------------------------------
@routes.route('/stornieren/<int:reservierungsnummer>', methods=['POST'])
@login_required
def stornieren(reservierungsnummer):
    reservation = Reserviert.query.get_or_404(reservierungsnummer)
    if reservation.kunden_nr == current_user.id:
        db.session.delete(reservation)
        db.session.commit()
    return redirect(url_for('routes.reservierungen'))

# -----------------------------------
# Seminardetails anzeigen
# -----------------------------------
@routes.route('/seminar/<datum>/<uhrzeit>')
def seminar_details(datum, uhrzeit):
    seminar = Seminar.query.filter_by(datum=datum, uhrzeit=uhrzeit).first()
    return render_template('seminar_details.html', seminar=seminar)

# -----------------------------------
# Benutzerprofil bearbeiten
# -----------------------------------
@routes.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.vorname = request.form['vorname']
        current_user.nachname = request.form['nachname']
        current_user.plz = request.form['plz']
        current_user.ort = request.form['ort']
        current_user.strasse = request.form['strasse']
        current_user.hausnr = request.form['hausnr']
        
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('edit_user.html')

# -----------------------------------
# Logout Route
# -----------------------------------
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
