from app import db


def get_db():
    try:
        yield db.session
    finally:
        db.session.close()
