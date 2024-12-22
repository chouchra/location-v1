# location_app/rentals/routes.py

from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Rental, Product, Notification
from location_app.rentals.forms import RentalForm
from location_app.utils import roles_required

rentals_bp = Blueprint('rentals', __name__, template_folder='templates/rentals')

@rentals_bp.route('/')
@roles_required('client', 'admin')  # Admins peuvent voir toutes les locations
def list_rentals():
    if current_user.role == 'client':
        rentals = Rental.query.filter_by(user_id=current_user.id).order_by(Rental.created_at.desc()).all()
    elif current_user.role == 'admin':
        rentals = Rental.query.order_by(Rental.created_at.desc()).all()
    else:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('rentals/rental.html', rentals=rentals) 
    
@rentals_bp.route('/rent/<int:product_id>', methods=['GET', 'POST'])
@login_required
@roles_required('client')  # Seuls les clients peuvent louer
def rent_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = RentalForm()
    if form.validate_on_submit():
        days = form.days.data
        # Créer une nouvelle location
        rental = Rental(
            user_id=current_user.id,
            product_id=product.id,
            days=days,
            status='pending'
        )
        db.session.add(rental)
        db.session.commit()  # Commit avant d'utiliser rental.id

        # Ajouter une notification pour le fournisseur avec rental_id
        notification = Notification(
            user_id=product.supplier_id,
            message=f"Nouvelle demande de location pour {product.name} par {current_user.username}.",
            rental_id=rental.id
        )
        db.session.add(notification)
        db.session.commit()

        flash('Demande de location envoyée avec succès.', 'success')
        return redirect(url_for('main.home'))
    return render_template('rentals/rent_product.html', form=form, product=product)
