import logging

from flask import Blueprint, jsonify, request
from models import Contact, SpamLikelihood, User
from sqlalchemy import or_

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

search_bp = Blueprint("search", __name__)


@search_bp.route("/by_name", methods=["GET"])
def search_by_name():
    try:
        query = request.args.get("query")
        if not query:
            return jsonify({"message": "Query parameter is required"}), 400

        results = (
            User.query.filter(
                or_(User.name.like(f"{query}%"), User.name.like(f"%{query}%"))
            )
            .order_by(
                User.name.like(f"{query}%").desc(), User.name.like(f"%{query}%").desc()
            )
            .all()
        )

        response = [
            {
                "name": u.name,
                "phone_number": u.phone_number,
                "spam_likelihood": get_spam_likelihood(u.phone_number),
            }
            for u in results
        ]
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error searching by name: {e}")
        return jsonify({"message": "An error occurred while searching by name"}), 500


@search_bp.route("/by_phone", methods=["GET"])
def search_by_phone():
    try:
        query = request.args.get("query")
        if not query:
            return jsonify({"message": "Query parameter is required"}), 400

        results = (
            Contact.query.filter(Contact.phone_number.like(f"%{query}%"))
            .order_by(
                Contact.phone_number.like(f"{query}%").desc(),
                Contact.phone_number.like(f"%{query}%").desc(),
            )
            .all()
        )

        response = [
            {
                "name": c.name,
                "phone_number": c.phone_number,
                "spam_likelihood": get_spam_likelihood(c.phone_number),
            }
            for c in results
        ]
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error searching by phone: {e}")
        return jsonify({"message": "An error occurred while searching by phone"}), 500


def get_spam_likelihood(phone_number):
    spam_likelihood = SpamLikelihood.query.get(phone_number)
    return spam_likelihood.spam_count if spam_likelihood else 0
