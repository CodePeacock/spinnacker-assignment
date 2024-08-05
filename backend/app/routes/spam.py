import logging

from flask import Blueprint, jsonify, request
from models import Spam, SpamLikelihood, User
from routes import db

logger = logging.getLogger(__name__)

spam_bp = Blueprint("spam", __name__)


@spam_bp.route("/mark", methods=["POST"])
def mark_spam():
    try:
        data = request.json
        user_id = data["user_id"]
        phone_number = data["phone_number"]
        is_spam = data["isSpam"]

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found."}), 404

        if is_spam:
            mark_as_spam(user_id, phone_number)
        else:
            unmark_as_spam(user_id, phone_number)

        db.session.commit()

        # Return updated list of spam phone numbers
        spam_numbers = [
            spam.phone_number
            for spam in Spam.query.filter_by(marked_as_spam_by=user_id).all()
        ]
        return jsonify(spam_numbers), 200
    except Exception as e:
        logger.error(f"Error marking spam: {e}")
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


def mark_as_spam(user_id, phone_number):
    spam = Spam(phone_number=phone_number, marked_as_spam_by=user_id)
    db.session.add(spam)
    likelihood = SpamLikelihood.query.get(phone_number)
    if likelihood:
        likelihood.spam_count += 1
    else:
        likelihood = SpamLikelihood(phone_number=phone_number, spam_count=1)
        db.session.add(likelihood)


def unmark_as_spam(user_id, phone_number):
    Spam.query.filter_by(phone_number=phone_number, marked_as_spam_by=user_id).delete()
    likelihood = SpamLikelihood.query.get(phone_number)
    if likelihood and likelihood.spam_count > 0:
        likelihood.spam_count -= 1
        if likelihood.spam_count == 0:
            db.session.delete(likelihood)
