from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from location_app import db
from location_app.models import Product
from location_app.utils import roles_required
from location_app.products.forms import ProductForm

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
@login_required
def list_products():
    if current_user.role == 'supplier':
        products = Product.query.filter_by(supplier_id=current_user.id).all()
    elif current_user.role == 'admin' or current_user.role == 'client':
        products = Product.query.all()
    else:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('products/product.html', products=products)

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
@roles_required('supplier')
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            daily_price=form.daily_price.data,
            supplier_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Produit ajouté avec succès.', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/add_product.html', form=form)

@products_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@roles_required('supplier')
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.supplier_id != current_user.id and current_user.role != 'admin':
        flash('Accès refusé.', 'danger')
        return redirect(url_for('products.list_products'))
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.daily_price = form.daily_price.data
        db.session.commit()
        flash('Produit mis à jour avec succès.', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/edit_product.html', form=form, product=product)

@products_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
@roles_required('supplier')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.supplier_id != current_user.id and current_user.role != 'admin':
        flash('Accès refusé.', 'danger')
        return redirect(url_for('products.list_products'))
    db.session.delete(product)
    db.session.commit()
    flash('Produit supprimé avec succès.', 'success')
    return redirect(url_for('products.list_products'))
