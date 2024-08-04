"""
This file contains the routes for user registration, email verification, and login.

Functions:
    register: Registers a new user in the database.
    verify: Verifies the user's email using an OTP.
    login: Logs in a user if the credentials are valid and the account is verified.
    send_otp: Sends an OTP to the user's email for verification.
    _auth_send_otp_email: Sends the OTP email using the SMTP server.
"""

import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, jsonify, request
from flask_praetorian import auth_required
from models import User
from otp import generate_otp
from routes import db, guard

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
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
    user.otp_expiration = datetime.now(timezone.utc) + timedelta(minutes=10)
    db.session.commit()

    return jsonify(
        {"message": "User registered successfully. Please verify your email."}
    ), 201


@auth_bp.route("/login", methods=["POST"])
@auth_required
def login():
    data = request.json or None
    password = data["password"]
    user = User.query.filter_by(email=data["email"], verified=True).first()
    if user and guard.authenticate(username=data["email"], password=password):
        return jsonify(
            {"access_token": guard.encode_jwt_token(user), "user_id": user.id}
        ), 200
    return jsonify({"message": "Invalid credentials or unverified account."}), 401


@auth_bp.route("/verify", methods=["POST"])
def verify():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and user.otp == data["otp"]:
        user.verified = True
        user.otp = None  # Clear OTP after verification
        db.session.commit()
        return jsonify({"success": True, "message": "User verified successfully."}), 200
    return jsonify({"success": False, "message": "Invalid OTP."}), 400


@auth_bp.route("/api/refresh", methods=["POST"])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    """
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {"access_token": new_token}
    return ret, 200


def send_otp(email):
    # Generate OTP
    otp = generate_otp()

    # Email body
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

    # Email setup
    sender_email = os.environ.get(
        "EMAIL_USER"
    )  # Ensure this is set in your environment
    sender_password = os.environ.get(
        "EMAIL_PASSWORD"
    )  # Ensure this is set in your environment
    subject = "Your OTP Code for Email Verification"

    # MIME setup
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    # Attach the HTML body to the email
    msg.attach(MIMEText(body, "html"))

    try:
        _auth_send_otp_email(sender_email, sender_password, msg, email)
    except Exception as e:
        print(f"Failed to send OTP email: {e}")

    return otp


# TODO Rename this here and in `send_otp`
def _auth_send_otp_email(sender_email, sender_password, msg, email):
    # SMTP server configuration
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.send_message(msg)
    server.quit()
    print(f"OTP email sent successfully to {email}")
