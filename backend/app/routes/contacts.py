from flask import Blueprint, jsonify, request
from models import Contact, User
from routes import db

contacts_bp = Blueprint("contacts", __name__)


@contacts_bp.route("/add", methods=["POST"])
def add_contact():
    try:
        data = request.json
        if user := User.query.get(data["user_id"]):
            contact = Contact(
                name=data["name"], phone_number=data["phone_number"], user_id=user.id
            )
            db.session.add(contact)
            db.session.commit()
            return jsonify({"message": "Contact added successfully."}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    return jsonify({"message": "User not found."}), 404


@contacts_bp.route("/list/<int:user_id>", methods=["GET"])
def list_contacts(user_id):
    if user := User.query.get(user_id):
        contacts = Contact.query.filter_by(user_id=user_id).all()
        return jsonify(
            [{"name": c.name, "phone_number": c.phone_number} for c in contacts]
        ), 200
    return jsonify({"message": "User not found."}), 404
