from flask import Blueprint, jsonify, request
from models import Contact, SpamLikelihood, User
from sqlalchemy import func, or_

search_bp = Blueprint("search", __name__)


def get_relevance_score(query, name, phone_number):
    return (
        func.length(name) - func.length(query),
        func.length(phone_number) - func.length(query),
    )


@search_bp.route("/search_database", methods=["GET"])
def search():
    try:
        query = request.args.get("query")
        results = (
            User.query.filter(
                or_(
                    User.name.ilike(f"%{query}%"), User.phone_number.ilike(f"%{query}%")
                )
            )
            .order_by(get_relevance_score(query, User.name, User.phone_number))
            .all()
        ) + (
            Contact.query.filter(
                or_(
                    Contact.name.ilike(f"%{query}%"),
                    Contact.phone_number.ilike(f"%{query}%"),
                )
            )
            .order_by(get_relevance_score(query, Contact.name, Contact.phone_number))
            .all()
        )
        combined_results = [
            {
                "name": r.name,
                "phone_number": r.phone_number,
                "spam_likelihood": SpamLikelihood.query.get(r.phone_number).spam_count
                if SpamLikelihood.query.get(r.phone_number)
                else 0,
            }
            for r in results
        ]
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    return jsonify(combined_results), 200
