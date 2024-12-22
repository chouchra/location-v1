from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from location_app import db
from location_app.models import User, Product
from location_app.utils import roles_required
from location_app.admin.forms import UserRoleForm

admin_bp = Blueprint('admin', __name__ )

@admin_bp.route('/dashboard')
@login_required
@roles_required('admin')
def dashboard():
    users = User.query.all()
    products = Product.query.all()
    return render_template('admin/dashboard.html', users=users, products=products)

@admin_bp.route('/promote/<int:user_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserRoleForm(obj=user)
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash('Rôle de l\'utilisateur mis à jour.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/promote_user.html', form=form, user=user)
