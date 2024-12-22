# location_app/notifications/routes.py

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Notification, Rental, User
from location_app.utils import roles_required

notifications_bp = Blueprint('notifications', __name__, template_folder='templates/notifications')

@notifications_bp.route('/')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications/notifications.html', notifications=notifications)

@notifications_bp.route('/accept/<int:notification_id>', methods=['POST'])
@login_required
@roles_required('supplier')
def accept_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    rental = Rental.query.get(notification.rental_id)
    
    if rental.status != 'pending':
        flash('Cette réservation a déjà été traitée.', 'warning')
        return redirect(url_for('notifications.notifications'))
    
    rental.status = 'accepted'
    db.session.commit()
    
    # Notifier le client
    client_notification = Notification(
        user_id=rental.user_id,
        message=f"Votre réservation #{rental.id} a été acceptée par le fournisseur.",
        rental_id=rental.id
    )
    db.session.add(client_notification)
    db.session.commit()
    
    # Marquer la notification comme lue
    notification.is_read = True
    db.session.commit()
    
    flash(f'Location #{rental.id} acceptée.', 'success')
    return redirect(url_for('notifications.notifications'))

@notifications_bp.route('/refuse/<int:notification_id>', methods=['POST'])
@login_required
@roles_required('supplier')
def refuse_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    rental = Rental.query.get(notification.rental_id)
    
    if rental.status != 'pending':
        flash('Cette réservation a déjà été traitée.', 'warning')
        return redirect(url_for('notifications.notifications'))
    
    rental.status = 'refused'
    db.session.commit()
    
    # Notifier le client
    client_notification = Notification(
        user_id=rental.user_id,
        message=f"Votre réservation #{rental.id} a été refusée par le fournisseur.",
        rental_id=rental.id
    )
    db.session.add(client_notification)
    db.session.commit()
    
    # Marquer la notification comme lue
    notification.is_read = True
    db.session.commit()
    
    flash(f'Location #{rental.id} refusée.', 'warning')
    return redirect(url_for('notifications.notifications'))
