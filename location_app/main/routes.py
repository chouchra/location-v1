# location_app/main/routes.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from location_app.models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    products = Product.query.all()
    return render_template('main/home.html', products=products)
