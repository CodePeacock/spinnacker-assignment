from flask import Blueprint, jsonify, request
from models import Contact, SpamLikelihood, User
from sqlalchemy import or_

search_bp = Blueprint("search", __name__)


@search_bp.route("/by_name", methods=["GET"])
def search_by_name():
    query = request.args.get("query")
    results = (
        User.query.filter(
            or_(User.name.like(f"{query}%"), User.name.like(f"%{query}%"))
        )
        .order_by(
            User.name.like(f"{query}%").desc(), User.name.like(f"%{query}%").desc()
        )
        .all()
    )
    return jsonify(
        [
            {
                "name": u.name,
                "phone_number": u.phone_number,
                "spam_likelihood": SpamLikelihood.query.get(u.phone_number).spam_count
                if SpamLikelihood.query.get(u.phone_number)
                else 0,
            }
            for u in results
        ]
    ), 200


@search_bp.route("/by_phone", methods=["GET"])
def search_by_phone():
    query = request.args.get("query")
    results = (
        Contact.query.filter(Contact.phone_number.like(f"%{query}%"))
        .order_by(
            Contact.phone_number.like(f"{query}%").desc(),
            Contact.phone_number.like(f"%{query}%").desc(),
        )
        .all()
    )
    return jsonify(
        [
            {
                "name": c.name,
                "phone_number": c.phone_number,
                "spam_likelihood": SpamLikelihood.query.get(c.phone_number).spam_count
                if SpamLikelihood.query.get(c.phone_number)
                else 0,
            }
            for c in results
        ]
    ), 200
