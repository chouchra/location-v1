# location_app/notifications/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Notification

notifications_bp = Blueprint('notifications', __name__ )

@notifications_bp.route('/')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications/notifications.html', notifications=notifications)

@notifications_bp.route('/mark_as_read/<int:notification_id>')
@login_required
def mark_as_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('notifications.notifications'))
    notification.is_read = True
    db.session.commit()
    flash('Notification marquée comme lue.', 'success')
    return redirect(url_for('notifications.notifications'))
