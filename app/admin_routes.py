"""
admin_routes.py – Enthält alle Routen für admin User
"""

from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import db, User, Teilnehmer, Ausbilder

# Blueprint für die Routen erstellen
admin_routes = Blueprint('admin_routes', __name__)

# -----------------------------------
# Funktion zur Initialisierung des Login-Managers
# -----------------------------------
@login_required
def load_user(user_id):
    return User.query.get(int(user_id))
