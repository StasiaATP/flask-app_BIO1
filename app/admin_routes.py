"""
admin_routes.py – Enthält alle Routen für admin User
"""

from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models import db, Person, Teilnehmer, Ausbilder, Kurs, Seminar, Organisator

# Blueprint für die Routen erstellen
admin_routes = Blueprint('admin_routes', __name__)

# -----------------------------------
# Überprüfung, ob der Nutzer ein Admin ist
# -----------------------------------
def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.username != 'admin':
            return redirect('/')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# -----------------------------------
# Alle User anzeigen (Admin-Ansicht)
# -----------------------------------
@admin_routes.route('/admin/user')
@admin_required
def admin_user():
    user = Person.query.all()
    return render_template('admin_user.html', user=user)

# -----------------------------------
# Alle Kurse und Seminare anzeigen (Admin-Ansicht)
# -----------------------------------
@admin_routes.route('/admin/kurse')
@admin_required
def admin_kurse():
    kurse = Kurs.query.all()
    seminare = Seminar.query.all()
    return render_template('admin_kurse.html', kurse=kurse, seminare=seminare)

# -----------------------------------
# Organisator anlegen
# -----------------------------------
@admin_routes.route('/admin/neuer_organisator', methods=['GET', 'POST'])
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
        telefonnummer = request.form['telefonnummer']

        # Organisator speichern
        organisator = Organisator(
                username=username,
                password=password,
                sozial_vers_nr=sozial_vers_nr,
                vorname=vorname,
                nachname=nachname,
                plz=plz,
                ort=ort,
                strasse=strasse,
                hausnr=hausnr,
                telefonnummer=telefonnummer
        )
        db.session.add(organisator)
        db.session.commit()

        return redirect('/admin/user')
    return render_template('admin_neuer_organisator.html')
