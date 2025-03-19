"""
teilnehmer_routes.py – Enthält alle Routes spezifisch für Teilnehmer
--------------------------------------------------------
"""

from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import db, User, Seminar, Reserviert

# Blueprint für die Routen erstellen
teilnehmer_routes = Blueprint('teilnehmer_routes', __name__)

# -----------------------------------
# Funktion zur Initialisierung des Login-Managers
# -----------------------------------
@login_required
def load_user(user_id):
    return User.query.get(int(user_id))

# -----------------------------------
# Reservierung eines Seminars
# -----------------------------------
@teilnehmer_routes.route('/reserve', methods=['GET', 'POST'])
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
                return redirect('/reservierungen') # leite weiter zu Reservierungen
    seminars = Seminar.query.all()
    return render_template('reserve.html', seminars=seminars)

# -----------------------------------
# Liste der Reservierungen anzeigen
# -----------------------------------
@teilnehmer_routes.route('/reservierungen')
@login_required
def reservierungen():
    user_reservations = Reserviert.query.filter_by(kunden_nr=current_user.id).all()
    return render_template('reservierungen.html', reservations=user_reservations)

# -----------------------------------
# Stornieren einer Reservierung
# -----------------------------------
@teilnehmer_routes.route('/stornieren/<int:reservierungsnummer>', methods=['POST'])
@login_required
def stornieren(reservierungsnummer):
    reservation = Reserviert.query.get_or_404(reservierungsnummer)
    if reservation.kunden_nr == current_user.id:
        db.session.delete(reservation)
        db.session.commit()
    return redirect('/reservierungen')

# -----------------------------------
# Seminardetails anzeigen
# -----------------------------------
@teilnehmer_routes.route('/seminar/<datum>/<uhrzeit>')
def seminar_details(datum, uhrzeit):
    seminar = Seminar.query.filter_by(datum=datum, uhrzeit=uhrzeit).first()
    return render_template('seminar_details.html', seminar=seminar)

