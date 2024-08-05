import os

from models import User
from routes import create_app, db, guard

if __name__ == "__main__":
    app = create_app()
    guard.init_app(app, User)

    @app.before_request
    def create_table():
        db.create_all()

    # Check if the environment variable FLASK_ENV is set to 'production'
    is_production = os.getenv("FLASK_ENV") == "production"

    app.run(debug=not is_production, host="0.0.0.0", port=5000)
