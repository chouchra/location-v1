# location_app/supplier/__init__.py

from flask import Blueprint

# Définition du blueprint supplier
supplier_bp = Blueprint('supplier', __name__, template_folder='templates/supplier')

# Importer les routes après la définition du blueprint pour éviter les erreurs
from location_app.supplier import routes
