import logging

from flask import Blueprint, jsonify
from flask_cors import CORS
from routes.auth import auth_bp
from routes.contacts import contacts_bp
from routes.search import search_bp
from routes.spam import spam_bp

# Initialize the main blueprint
main_bp = Blueprint("main", __name__)

# Enable CORS
CORS(main_bp)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@main_bp.route("/")
def index():
    logger.info("Index route accessed")
    return "Welcome to the Contact Management API"


# Register blueprints
main_bp.register_blueprint(auth_bp, url_prefix="/auth")
main_bp.register_blueprint(contacts_bp, url_prefix="/contacts")
main_bp.register_blueprint(spam_bp, url_prefix="/spam")
main_bp.register_blueprint(search_bp, url_prefix="/search")


# Centralized error handler
@main_bp.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"An error occurred: {e}")
    response = {
        "error": str(e),
        "message": "An internal error occurred. Please try again later.",
    }
    return jsonify(response), 500
