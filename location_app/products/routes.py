# location_app/products/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
@login_required
def list_products():
    products = Product.query.all()
    return render_template('products/product.html', products=products)

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'supplier':
        flash('Accès réservé aux fournisseurs.', 'danger')
        return redirect(url_for('products.list_products'))
    if request.method == 'POST':
        name = request.form.get('name')
        daily_price = request.form.get('daily_price')
        if not name or not daily_price:
            flash('Veuillez remplir tous les champs.', 'danger')
            return redirect(url_for('products.add_product'))
        product = Product(name=name, daily_price=float(daily_price), supplier_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        flash('Produit ajouté avec succès.', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/add_product.html')
