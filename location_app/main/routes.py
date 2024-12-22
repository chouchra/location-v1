from flask import Blueprint, render_template
from flask_login import login_required
from location_app.models import Product
from sqlalchemy.orm import joinedload

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    products = Product.query.options(joinedload(Product.supplier)).all()
    return render_template('main/home.html', products=products)

