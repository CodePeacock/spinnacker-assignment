from routes import create_app, db

if __name__ == "__main__":
    app = create_app()

    @app.before_request
    def create_table():
        db.create_all()

    app.run(debug=True)
