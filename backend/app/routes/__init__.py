"""
This file is used to import all the routes in the app.
"""

from config import Config
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_praetorian import Praetorian
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
guard = Praetorian()


def create_app():
    app = Flask(__name__)
    Mail(app)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from routes.auth import auth_bp
        from routing import main_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

    return app
