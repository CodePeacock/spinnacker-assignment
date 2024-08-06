"""
This module contains the routes for user authentication, including registration, login, token refresh, and email verification. It also includes a function to send an OTP (One-Time Password) email for email verification.

"""

import logging
import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, jsonify, request
from models import User
from otp import generate_otp
from routes import db, guard

auth_bp = Blueprint("auth", __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    This function registers a new user by creating a User object with the provided data and storing it in the database.
    The user's password is hashed before storing it in the database.
    An OTP (One-Time Password) is generated and sent to the user's email for verification.

    Returns:
        A JSON response containing a success message if the registration is successful, or an error message if it fails.
    Raises:
        Exception: If an error occurs during the registration process.
    """
    try:
        data = request.json
        hashed_password = guard.hash_password(data["password"])  # Hash the password
        user = User(
            name=data["name"],
            phone_number=data["phone_number"],
            email=data["email"],
            password=hashed_password,  # Store the hashed password
            city=data.get("city"),
            country=data.get("country"),
        )
        db.session.add(user)
        db.session.commit()

        # Generate and send OTP
        otp = send_otp(user.email)
        user.otp = otp
        db.session.commit()

        return jsonify(
            {"message": "User registered successfully. Please verify your email."}
        ), 201
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates a user and generates an access token.

    Returns:
    If the user is authenticated successfully, returns a JSON response containing the access token and user ID.
    If the user authentication fails, returns a JSON response with an error message and a status code of 401.
    If an error occurs during the login process, returns a JSON response with an error message and a status code of 500.
    """
    # Code implementation
    # Error handling
    try:
        data = request.json
        password = data["password"]
        user = User.query.filter_by(email=data["email"], verified=True).first()
        if user and guard.authenticate(username=data["email"], password=password):
            access_token = guard.encode_jwt_token(user)
            return jsonify({"access_token": access_token, "user_id": user.id})
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify({"error": "Login failed"}), 500


@auth_bp.route("/refreshtoken", methods=["POST"])
def refresh():
    """
    Refreshes the JWT token.

    Returns:
        If the token refresh is successful and the user is verified, returns a JSON response with the new access token and the user ID.
        If the token is invalid, returns a JSON response with an error message and a status code of 401 (Unauthorized).
        If an error occurs during the token refresh, returns a JSON response with an error message and a status code of 500 (Internal Server Error).
    """
    try:
        old_token = request.get_json().get("token")
        new_token = guard.refresh_jwt_token(old_token)
        user_email = guard.extract_jwt_token(old_token)["email"]
        user = User.query.filter_by(email=user_email, verified=True).first()
        if user:
            return jsonify({"access_token": new_token, "user_id": user.id}), 200
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        logger.error(f"Error during token refresh: {e}")
        return jsonify({"error": "Token refresh failed"}), 500


@auth_bp.route("/verify", methods=["POST"])
def verify():
    """
    Verify user's OTP and update verification status.

    Returns:
        A JSON response containing the verification status and a message.

    Raises:
        Exception: If an error occurs during the verification process.
    """
    try:
        data = request.json
        user = User.query.filter_by(email=data["email"]).first()
        if (
            user
            and user.otp == data["otp"]
        ):
            user.verified = True
            user.otp = None  # Clear OTP after verification
            db.session.commit()
            return jsonify(
                {"success": True, "message": "User verified successfully."}
            ), 200
        return jsonify({"success": False, "message": "Invalid or expired OTP."}), 400
    except Exception as e:
        logger.error(f"Error during verification: {e}")
        return jsonify({"error": "Verification failed"}), 500


def send_otp(email):
    """
    Sends an OTP (One-Time Password) email to the specified email address for email verification.
    Parameters:
    - `email (str)`: The email address to send the OTP to.
    Returns:
    - `otp (str)`: The generated OTP code.
    Raises:
    - `Exception`: If there is an error sending the OTP email."""
    otp = generate_otp()
    body = f"""
    <html>
    <body>
        <h2>Your OTP Code</h2>
        <p>Dear User,</p>
        <p>Thank you for registering with us. Your One-Time Password (OTP) for email verification is:</p>
        <h1 style="color: #2e6c80;">{otp}</h1>
        <p>Please enter this code on the website to complete your registration.</p>
        <p>This OTP is valid for the next 10 minutes.</p>
        <br>
        <p>Best Regards,</p>
        <p>Your Company Name</p>
    </body>
    </html>
    """
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASSWORD")
    subject = "Your OTP Code for Email Verification"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        _auth_send_otp_email(sender_email, sender_password, msg, email)
    except Exception as e:
        logger.error(f"Failed to send OTP email: {e}")

    return otp


def _auth_send_otp_email(sender_email, sender_password, msg, email):
    """
    Sends an OTP email to the specified email address.

    Parameters:
    - sender_email (str): The email address of the sender.
    - sender_password (str): The password of the sender's email account.
    - msg (MIMEText): The message object containing the email content.
    - email (str): The email address of the recipient.

    Returns:
    None

    Raises:
    - Exception: If there is an error while sending the email.
    """
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        logger.info(f"OTP email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
