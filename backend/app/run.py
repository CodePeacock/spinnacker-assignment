"""This file is the entry point of the application. It creates the Flask app, initializes the Flask-JWT-Extended extension, and runs the app."""

import os

from flask_cors import CORS
from models import User
from routes import create_app, db, guard

app = create_app()
if __name__ == "__main__":
    guard.init_app(app, User)

    @app.before_request
    def create_table():
        db.create_all()

    # Check if the environment variable FLASK_ENV is set to 'production'
    environment_type = os.getenv("FLASK_ENV") == "production"

    allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
    CORS(app, resources={r"/*": {"origins": allowed_origins.split(",")}})

    app.run(debug=not environment_type, host="0.0.0.0", port=5000)
