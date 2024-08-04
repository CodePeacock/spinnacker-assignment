from flask import Blueprint, jsonify, request

from routes import db
from models import Spam, SpamLikelihood, User

spam_bp = Blueprint("spam", __name__)


@spam_bp.route("/mark", methods=["POST"])
def mark_spam():
    data = request.json
    if user := User.query.get(data["user_id"]):
        spam = Spam(phone_number=data["phone_number"], marked_as_spam_by=user.id)
        db.session.add(spam)
        db.session.commit()

        if likelihood := SpamLikelihood.query.get(data["phone_number"]):
            likelihood.spam_count += 1
        else:
            likelihood = SpamLikelihood(phone_number=data["phone_number"], spam_count=1)
            db.session.add(likelihood)
        db.session.commit()

        return jsonify({"message": "Number marked as spam."}), 201
    return jsonify({"message": "User not found."}), 404
