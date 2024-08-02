from flask import Blueprint

from auth import auth_bp
from contacts import contacts_bp
from search import search_bp
from spam import spam_bp

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return "Welcome to the Contact Management API"


main_bp.register_blueprint(auth_bp, url_prefix="/auth")
main_bp.register_blueprint(contacts_bp, url_prefix="/contacts")
main_bp.register_blueprint(spam_bp, url_prefix="/spam")
main_bp.register_blueprint(search_bp, url_prefix="/search")
