# location_app/supplier/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Rental, Product
from location_app.utils import roles_required
from location_app.supplier.forms import UpdateRentalForm

from . import supplier_bp  # Importer le blueprint supplier_bp défini dans __init__.py

@supplier_bp.route('/dashboard')
@login_required
@roles_required('supplier')  # Seuls les fournisseurs peuvent accéder
def dashboard():
    # Récupérer les locations liées aux produits du fournisseur en utilisant Product.supplier_id directement
    rentals_pending = Rental.query.join(Product).filter(
        Rental.status == 'pending',
        Product.supplier_id == current_user.id
    ).all()

    rentals_accepted = Rental.query.join(Product).filter(
        Rental.status == 'accepted',
        Product.supplier_id == current_user.id
    ).all()

    rentals_in_progress = Rental.query.join(Product).filter(
        Rental.status == 'in_progress',
        Product.supplier_id == current_user.id
    ).all()

    rentals_finished = Rental.query.join(Product).filter(
        Rental.status == 'finished',
        Product.supplier_id == current_user.id
    ).all()

    form = UpdateRentalForm()  # Instanciation du formulaire
    return render_template(
        'supplier/dashboard.html',
        rentals_pending=rentals_pending,
        rentals_accepted=rentals_accepted,
        rentals_in_progress=rentals_in_progress,
        rentals_finished=rentals_finished,
        form=form  # Passage du formulaire au template
    )

@supplier_bp.route('/rental/<int:rental_id>/update', methods=['POST'])
@login_required
@roles_required('supplier')  # Seuls les fournisseurs peuvent mettre à jour
def update_rental(rental_id):
    rental = Rental.query.get_or_404(rental_id)
    if rental.product.supplier_id != current_user.id:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('supplier.dashboard'))
    
    form = UpdateRentalForm()
    if form.validate_on_submit():
        action = form.action.data
        if action == 'accept':
            rental.status = 'accepted'
            flash('Location acceptée.', 'success')
        elif action == 'refuse':
            rental.status = 'refused'
            flash('Location refusée.', 'warning')
        elif action == 'start':
            rental.status = 'in_progress'
            flash('Location commencée.', 'info')
        elif action == 'complete':
            rental.status = 'finished'
            flash('Location terminée.', 'success')
        db.session.commit()
        return redirect(url_for('supplier.dashboard'))
    flash('Action invalide.', 'danger')
    return redirect(url_for('supplier.dashboard'))
