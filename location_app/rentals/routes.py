from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Rental, Product, Notification
from location_app.utils import roles_required

rentals_bp = Blueprint('rentals', __name__ )

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

@rentals_bp.route('/rent/<int:product_id>', methods=['POST'])
@login_required
@roles_required('client')  # Seuls les clients peuvent louer
def rent_product(product_id):
    product = Product.query.get_or_404(product_id)
    days = request.form.get('days', 1)
    try:
        days = int(days)
        if days < 1:
            raise ValueError
    except ValueError:
        flash('Nombre de jours invalide.', 'danger')
        return redirect(url_for('main.home'))
    
    # Créer une nouvelle location
    rental = Rental(
        user_id=current_user.id,
        product_id=product.id,
        days=days,
        status='pending'
    )
    db.session.add(rental)
    
    # Ajouter une notification pour le fournisseur
    notification = Notification(
        user_id=product.supplier_id,
        message=f"Nouvelle demande de location pour {product.name} par {current_user.username}."
    )
    db.session.add(notification)
    db.session.commit()
    
    flash('Demande de location envoyée avec succès.', 'success')
    return redirect(url_for('rentals.list_rentals'))
