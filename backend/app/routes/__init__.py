"""
This file is used to import all the routes in the app.
"""

import os

import pymysql
from config import Config
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_praetorian import Praetorian
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
migrate = Migrate()
guard = Praetorian()


def create_app():
    app = Flask(__name__)
    Mail(app)
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
    CORS(
        app,
        origins=allowed_origins,
    )
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from routes.auth import auth_bp
        from routing import main_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

    return app
