# location_app/__init__.py

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Importer les modèles après avoir initialisé db
    from location_app import models

    # Enregistrer les blueprints
    from location_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from location_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from location_app.products.routes import products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from location_app.rentals.routes import rentals_bp
    app.register_blueprint(rentals_bp, url_prefix='/rentals')

    from location_app.notifications.routes import notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/notifications')

    # Context Processor pour les notifications
    @app.context_processor
    def inject_notification_count():
        if 'user_id' in session:
            user = models.User.query.get(session['user_id'])
            if user:
                count = models.Notification.query.filter_by(user_id=user.id, is_read=False).count()
                return {'notification_count': count}
        return {'notification_count': 0}

    # Context Processor pour current_user
    @app.context_processor
    def inject_current_user():
        if 'user_id' in session:
            user = models.User.query.get(session['user_id'])
            return {'current_user': user}
        return {'current_user': None}

    return app
