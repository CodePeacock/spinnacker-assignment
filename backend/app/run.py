from models import User
from routes import create_app, db, guard

if __name__ == "__main__":
    app = create_app()
    guard.init_app(app, User)

    @app.before_request
    def create_table():
        db.create_all()

    app.run(debug=True)
