# location_app/notifications/__init__.py

from flask import Blueprint

notifications_bp = Blueprint('notifications', __name__, template_folder='templates/notifications')

from location_app.notifications import routes
