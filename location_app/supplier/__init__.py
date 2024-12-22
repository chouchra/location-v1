# location_app/supplier/__init__.py

from flask import Blueprint

supplier_bp = Blueprint('supplier', __name__, template_folder='templates/supplier')

from location_app.supplier import routes
