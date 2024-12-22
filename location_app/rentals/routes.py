# location_app/rentals/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Rental, Product, Notification

rentals_bp = Blueprint('rentals', __name__ )

@rentals_bp.route('/')
@login_required
def list_rentals():
    rentals = Rental.query.filter_by(user_id=current_user.id).order_by(Rental.created_at.desc()).all()
    return render_template('rentals/rental.html', rentals=rentals)

@rentals_bp.route('/rent/<int:product_id>', methods=['POST'])
@login_required
def rent_product(product_id):
    product = Product.query.get_or_404(product_id)
    rental = Rental(user_id=current_user.id, product_id=product.id, days=request.form.get('days', 1), status='pending')
    db.session.add(rental)
    # Ajouter une notification pour le fournisseur
    notification = Notification(user_id=product.supplier_id, message=f"Nouvelle demande de location pour {product.name}.")
    db.session.add(notification)
    db.session.commit()
    flash('Demande de location envoyée.', 'success')
    return redirect(url_for('rentals.list_rentals'))
