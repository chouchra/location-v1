# location_app/notifications/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Notification, Rental, Product
from location_app.utils import roles_required

notifications_bp = Blueprint('notifications', __name__, template_folder='templates/notifications')

@notifications_bp.route('/')
@login_required
@roles_required('supplier', 'admin')  # Admin peut aussi gérer les notifications
def notifications():
    # Récupérer les notifications non lues pour le fournisseur actuel
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    return render_template('notifications/notifications.html', notifications=notifications)

@notifications_bp.route('/<int:notification_id>/accept', methods=['POST'])
@login_required
@roles_required('supplier', 'admin')
def accept_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    rental = Rental.query.get(notification.rental_id)
    if not rental:
        flash('Réservation introuvable.', 'danger')
        return redirect(url_for('notifications.notifications'))
    
    if rental.status != 'pending':
        flash('Cette réservation a déjà été traitée.', 'warning')
        return redirect(url_for('notifications.notifications'))
    
    rental.status = 'accepted'
    db.session.commit()
    
    # Marquer la notification comme lue
    notification.is_read = True
    db.session.commit()
    
    flash(f'Location #{rental.id} acceptée.', 'success')
    return redirect(url_for('notifications.notifications'))

@notifications_bp.route('/<int:notification_id>/refuse', methods=['POST'])
@login_required
@roles_required('supplier', 'admin')
def refuse_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    rental = Rental.query.get(notification.rental_id)
    if not rental:
        flash('Réservation introuvable.', 'danger')
        return redirect(url_for('notifications.notifications'))
    
    if rental.status != 'pending':
        flash('Cette réservation a déjà été traitée.', 'warning')
        return redirect(url_for('notifications.notifications'))
    
    rental.status = 'refused'
    db.session.commit()
    
    # Marquer la notification comme lue
    notification.is_read = True
    db.session.commit()
    
    flash(f'Location #{rental.id} refusée.', 'warning')
    return redirect(url_for('notifications.notifications'))
