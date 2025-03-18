from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db, User, Teilnehmer, Seminar, Reserviert, Ausbilder, BildetAus, Person, Kurs, KannAbhalten
from datetime import datetime

# Blueprint für die Routen erstellen
ausbilder_routes = Blueprint('ausbilder_routes', __name__)

# -----------------------------------
# von Ausbilder geleitete Seminare anzeigen
# -----------------------------------
@ausbilder_routes.route('/ausbilder_seminare')
@login_required
def geleitete_seminare_zeigen():
    geleitete_seminare = BildetAus.query.filter_by(ausbilder_kennzeichnung=current_user.kennzeichnung).all()
    return render_template('ausbilder_seminare.html', seminare=geleitete_seminare)


# -----------------------------------
# Teilnehmer anzeigen von Seminar
# -----------------------------------
@ausbilder_routes.route('/teilnehmer/<int:seminar_id>')
@login_required
def teilnehmer_anzeigen(seminar_id):
    #Teilnehmer von Seminar abfragen
    reservierungen = Reserviert.query.filter_by(seminar_id=seminar_id).all()
    if not reservierungen:
        personen = []
    else:
        
        kunden_nrs = [r.kunden_nr for r in reservierungen]  # Liste von Kundennummern
        teilnehmer = Teilnehmer.query.filter(Teilnehmer.kunden_nr.in_(kunden_nrs)).all() #Teilnehmer von Teilnehmer tabelle mit entsprechenden Kunden-Nrn
        sv_nrs = [t.sozial_vers_nr for t in teilnehmer]  # Liste von SV-Nummern
        personen = Person.query.filter(Person.sozial_vers_nr.in_(sv_nrs)).all()

    return render_template('ausbilder_teilnehmer_anzeigen.html', personen=personen)

# -----------------------------------
# Seminar ändern
# -----------------------------------
@ausbilder_routes.route('/seminar_aendern/<int:seminar_id>', methods=['GET', 'POST'])
@login_required
def seminar_aendern(seminar_id):
    error_message = None
    seminar = Seminar.query.get_or_404(seminar_id)

    if request.method == 'POST':
        datum_uhrzeit_str = request.form['Datum Uhrzeit']
        strasse = request.form['Strasse']
        hausnr = request.form['Hausnummer']
        plz = request.form['PLZ']

        # Converting datum string into datetime format
        try:
            datum_uhrzeit = datetime.strptime(datum_uhrzeit_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            error_message = 'Ungültiges Datum/Zeit Format.'
            return render_template('ausbilder_seminar_aendern.html', error_message=error_message, seminar=seminar)
        
        seminar.datum_uhrzeit = datum_uhrzeit
        seminar.strasse = strasse
        seminar.hausnr = hausnr
        seminar.plz = plz

        db.session.commit()

        return redirect(url_for('ausbilder_routes.geleitete_seminare_zeigen'))
    
    return render_template('ausbilder_seminar_aendern.html', seminar=seminar)


# -----------------------------------
# Seminar löschen
# -----------------------------------
@ausbilder_routes.route('/seminar_loeschen/<int:seminar_id>', methods=['POST'])
@login_required
def seminar_loeschen(seminar_id):
    seminar = Seminar.query.get_or_404(seminar_id)

    BildetAus.query.filter_by(seminar_id=seminar_id).delete()

    db.session.delete(seminar)
    db.session.commit()

    return redirect(url_for('ausbilder_routes.geleitete_seminare_zeigen'))


# -----------------------------------
# Neues Seminar erstellen
# -----------------------------------
@ausbilder_routes.route('/ausbilder_seminar_erstellen', methods=['GET', 'POST'])
@login_required
def seminar_erstellen():
    error_message = None

    # Get Kursname which of the current user can be an instructor. 
    # The values will appear in the dropdown-menu when creating a new Seminar
    kurs_names = KannAbhalten.query.filter_by(ausbilder_kennzeichnung=current_user.kennzeichnung).with_entities(KannAbhalten.kursname).distinct().all()
    if request.method == 'POST':
        id = request.form['Seminar id']
        datum_uhrzeit_str = request.form['Datum Uhrzeit']
        strasse = request.form['Strasse']
        hausnr = request.form['Hausnummer']
        plz = request.form['PLZ']
        kursname = request.form['Kurs']

        # checking if ID already exists in the table
        existing_seminar = Seminar.query.filter_by(id=id).first()

        if existing_seminar:
            # if ID exists, define error message
            error_message = 'Ein Seminar mit dieser ID existiert bereits.'
        
        # Converting datum string into datetime format
        try:
            datum_uhrzeit = datetime.strptime(datum_uhrzeit_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            error_message = 'Ungültiges Datum/Zeit Format.'
            return render_template('ausbilder_seminar_erstellen.html', error_message=error_message, kurs_names=kurs_names)

        if not error_message:
            neues_seminar = Seminar(
                id=id,
                datum_uhrzeit=datum_uhrzeit,
                strasse=strasse,
                hausnr=hausnr,
                plz=plz,
                kursname=kursname
            )
            db.session.add(neues_seminar)
            db.session.commit()

            neu_bildet_aus = BildetAus(
                seminar_id=id,
                ausbilder_kennzeichnung=current_user.kennzeichnung
            )
            db.session.add(neu_bildet_aus)
            db.session.commit()

            return redirect(url_for('routes.index'))
    
    return render_template('ausbilder_seminar_erstellen.html', error_message=error_message, kurs_names=kurs_names)
