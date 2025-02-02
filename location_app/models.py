# location_app/models.py

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from location_app import db, login

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    trust_index = db.Column(db.Integer, default=5)
    role = db.Column(db.String(32), default="client")  # Rôles : client, supplier, admin

    rentals = db.relationship('Rental', back_populates='user', lazy=True)
    notifications = db.relationship('Notification', back_populates='user', lazy=True)
    products = db.relationship('Product', back_populates='supplier', lazy=True)  # Pour les fournisseurs

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}, role={self.role}>"

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    daily_price = db.Column(db.Float, default=0.0)
    avg_rating_product = db.Column(db.Float, default=0.0)  # Champ pour la moyenne des notes
    supplier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Référence à l'utilisateur fournisseur
    image_url = db.Column(db.String(255), nullable=True)  # Nouveau champ pour l'image du produit

    rentals = db.relationship('Rental', back_populates='product', lazy=True)
    supplier = db.relationship('User', back_populates='products')  # Relation vers le fournisseur

    def __repr__(self):
        return f"<Product {self.name}>"

class Rental(db.Model):
    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    days = db.Column(db.Integer, default=1)
    start_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(32), default="pending")  # Status : pending, accepted, refused, in_progress, finished, dispute, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    dispute_reason = db.Column(db.String(255), nullable=True)
    dispute_comment = db.Column(db.Text, nullable=True)
    product_rating = db.Column(db.Integer, nullable=True)
    supplier_rating = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', back_populates='rentals')
    product = db.relationship('Product', back_populates='rentals')
    notifications = db.relationship('Notification', back_populates='rental', lazy=True)

    def __repr__(self):
        return f"<Rental #{self.id}, status={self.status}>"

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rental_id = db.Column(db.Integer, db.ForeignKey('rentals.id'), nullable=True)  # Nouveau champ

    user = db.relationship('User', back_populates='notifications')
    rental = db.relationship('Rental', back_populates='notifications')  # Relation avec Rental

    def __repr__(self):
        return f"<Notification {self.id} user={self.user_id} is_read={self.is_read}>"
