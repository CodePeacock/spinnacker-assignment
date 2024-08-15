"""
This module contains the routes for adding a new contact, fetching the username of a user, and listing contacts.
"""

from logging import INFO, basicConfig, getLogger

from flask import Blueprint, jsonify, request
from models import Contact, Spam, User
from routes import db

# Set up logging
basicConfig(level=INFO)
logger = getLogger(__name__)

contacts_bp = Blueprint("contacts", __name__)


@contacts_bp.route("/add", methods=["POST"])
def add_contact():
    """
    Adds a new contact to the database.

    Returns:

    - A JSON response containing a success message and status code 201 if the contact is added successfully.
    - A JSON response containing an error message and status code 404 if the user is not found.
    - A JSON response containing an error message and status code 409 if the contact already exists for the user.
    - A JSON response containing an error message and status code 500 if an error occurs while adding the contact.
    """
    try:
        data = request.json
        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"message": "User not found."}), 404

        # Check if the contact already exists for the user
        existing_contact = Contact.query.filter_by(
            user_id=user.id, phone_number=data["phone_number"]
        ).first()
        if existing_contact:
            return jsonify({"message": "Contact already exists for this user."}), 409

        # Check if the contact is added by someone else
        other_user_contact = Contact.query.filter_by(
            phone_number=data["phone_number"]
        ).first()
        contact_added_by_other = other_user_contact is not None

        contact = Contact(
            name=data["name"], phone_number=data["phone_number"], user_id=user.id
        )
        db.session.add(contact)
        db.session.commit()

        response_message = "Contact added successfully."
        if contact_added_by_other:
            response_message += " This user is added by someone already."

        return jsonify({"message": response_message}), 201
    except Exception as e:
        logger.error(f"Error adding contact: {e}")
        return jsonify({"message": "An error occurred while adding the contact."}), 500


@contacts_bp.route("/username/<int:user_id>", methods=["GET"])
def get_username(user_id):
    """
    Retrieves the username of a user based on the given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        A JSON response containing the user's name if the user is found.
        If the user is not found, a JSON response with a "User not found" message and a 404 status code is returned.
        If an error occurs while fetching the username, a JSON response with an error message and a 500 status code is returned.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found."}), 404
        return jsonify({"name": user.name}), 200
    except Exception as e:
        logger.error(f"Error fetching username: {e}")
        return jsonify(
            {"message": "An error occurred while fetching the username."}
        ), 500


@contacts_bp.route("/list/<int:user_id>", methods=["GET"])
def list_contacts(user_id):
    """
    Retrieves a list of contacts for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: A tuple containing the JSON response and the status code.
        The JSON response is a list of contacts, where each contact is represented as a dictionary
        with the following keys:
        - name (str): The name of the contact.
        - phone_number (str): The phone number of the contact.
        - is_spam (bool): Indicates whether the contact is marked as spam.

    The status code indicates the success or failure of the request:
        - 200: Success.
        - 404: User not found.
        - 500: An error occurred while listing the contacts.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found."}), 404

        contacts = Contact.query.filter_by(user_id=user_id).all()
        spam_numbers = [
            spam.phone_number
            for spam in Spam.query.filter_by(marked_as_spam_by=user_id).all()
        ]
        contact_list = [
            {
                "id": c.id,
                "name": c.name,
                "phone_number": c.phone_number,
                "is_spam": c.phone_number in spam_numbers,
            }
            for c in contacts
        ]
        return jsonify(contact_list), 200
    except Exception as e:
        logger.error(f"Error listing contacts: {e}")
        return jsonify(
            {"message": "An error occurred while listing the contacts."}
        ), 500


@contacts_bp.route("/delete/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    """
    Deletes a contact from the database.

    Args:
        contact_id (int): The ID of the contact to be deleted.

    Returns:
        A JSON response containing a success message and status code 200 if the contact is deleted successfully.
        A JSON response containing an error message and status code 404 if the contact is not found.
        A JSON response containing an error message and status code 500 if an error occurs while deleting the contact.
    """
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({"message": "Contact not found."}), 404

        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contact deleted successfully."}), 200
    except Exception as e:
        logger.error(f"Error deleting contact: {e}")
        db.session.rollback()
        return jsonify(
            {"message": "An error occurred while deleting the contact."}
        ), 500
