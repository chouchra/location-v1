from flask import Blueprint, render_template
from flask_login import login_required
from location_app.models import Product
from location_app.rentals.forms import RentForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    products = Product.query.all()
    rent_form = RentForm()
    return render_template('main/home.html', products=products, rent_form=rent_form)
