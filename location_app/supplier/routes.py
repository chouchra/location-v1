# location_app/supplier/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Rental, Product, Notification
from location_app.utils import roles_required

supplier_bp = Blueprint('supplier', __name__, template_folder='templates/supplier')

@supplier_bp.route('/dashboard')
@login_required
@roles_required('supplier')
def dashboard():
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

    return render_template(
        'supplier/dashboard.html',
        rentals_pending=rentals_pending,
        rentals_accepted=rentals_accepted,
        rentals_in_progress=rentals_in_progress,
        rentals_finished=rentals_finished
    )

@supplier_bp.route('/start/<int:rental_id>', methods=['POST'])
@login_required
@roles_required('supplier')
def start_rental(rental_id):
    rental = Rental.query.get_or_404(rental_id)
    if rental.status != 'accepted':
        flash('Cette location ne peut pas être commencée.', 'warning')
        return redirect(url_for('supplier.dashboard'))
    
    rental.status = 'in_progress'
    db.session.commit()

    # Notifier le client
    client_notification = Notification(
        user_id=rental.user_id,
        message=f"Votre location #{rental.id} a commencé.",
        rental_id=rental.id
    )
    db.session.add(client_notification)
    db.session.commit()

    flash(f'Location #{rental.id} commencée.', 'info')
    return redirect(url_for('supplier.dashboard'))

@supplier_bp.route('/complete/<int:rental_id>', methods=['POST'])
@login_required
@roles_required('supplier')
def complete_rental(rental_id):
    rental = Rental.query.get_or_404(rental_id)
    if rental.status != 'in_progress':
        flash('Cette location ne peut pas être terminée.', 'warning')
        return redirect(url_for('supplier.dashboard'))
    
    rental.status = 'finished'
    db.session.commit()

    # Notifier le client
    client_notification = Notification(
        user_id=rental.user_id,
        message=f"Votre location #{rental.id} est terminée.",
        rental_id=rental.id
    )
    db.session.add(client_notification)
    db.session.commit()

    flash(f'Location #{rental.id} terminée.', 'success')
    return redirect(url_for('supplier.dashboard'))
