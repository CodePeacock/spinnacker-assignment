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
        user.otp_expiration = datetime.now(timezone.utc) + timedelta(minutes=10)
        db.session.commit()

        return jsonify(
            {"message": "User registered successfully. Please verify your email."}
        ), 201
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
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
    try:
        data = request.json
        user = User.query.filter_by(email=data["email"]).first()
        if (
            user
            and user.otp == data["otp"]
            and user.otp_expiration > datetime.now(timezone.utc)
        ):
            user.verified = True
            user.otp = None  # Clear OTP after verification
            user.otp_expiration = None
            db.session.commit()
            return jsonify(
                {"success": True, "message": "User verified successfully."}
            ), 200
        return jsonify({"success": False, "message": "Invalid or expired OTP."}), 400
    except Exception as e:
        logger.error(f"Error during verification: {e}")
        return jsonify({"error": "Verification failed"}), 500


def send_otp(email):
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
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        logger.info(f"OTP email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
