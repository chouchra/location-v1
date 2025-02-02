# location_app/main/routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from location_app.models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    search_query = request.args.get('search', '')
    if search_query:
        # Recherche des produits par nom (case-insensitive)
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()
    else:
        products = Product.query.all()
    return render_template('main/home.html', products=products, search_query=search_query)
