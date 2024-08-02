import hashlib
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from __init__ import db
from flask import Blueprint, jsonify, request
from models import User
from otp import generate_otp

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = hashlib.sha256(data["password"].encode()).hexdigest()
    user = User(
        name=data["name"],
        phone_number=data["phone_number"],
        email=data["email"],
        password=hashed_password,
        city=data.get("city"),
        country=data.get("country"),
    )
    db.session.add(user)
    db.session.commit()
    send_otp(user.email)
    return jsonify(
        {"message": "User registered successfully. Please verify your email."}
    ), 201


@auth_bp.route("/verify", methods=["POST"])
def verify():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and data["otp"] == "123456":  # Simplified for example
        user.verified = True
        db.session.commit()
        return jsonify({"message": "User verified successfully."}), 200
    return jsonify({"message": "Invalid OTP."}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or None
    hashed_password = hashlib.sha256(data["password"].encode()).hexdigest()
    if user := User.query.filter_by(
        email=data["email"], password=hashed_password, verified=True
    ).first():
        return jsonify({"message": "Login successful.", "user_id": user.id}), 200
    return jsonify({"message": "Invalid credentials or unverified account."}), 401


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
    print(f"Logging in with {sender_email} and {sender_password}")
    server.login(sender_email, sender_password)

    # Send the email
    server.send_message(msg)
    server.quit()
    print(f"OTP email sent successfully to {email}")
