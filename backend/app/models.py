"""
This module contains the models for the application that are used to interact with the database.
"""

from routes import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    # Store the hashed password that is longer than 128 characters
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    city = db.Column(db.String(128), nullable=True)
    country = db.Column(db.String(128), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    otp = db.Column(db.String(6), nullable=True)
    roles = db.Column(db.Text, nullable=True)

    @property
    def rolenames(self):
        return self.roles.split(",") if self.roles else []

    @classmethod
    def lookup(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="contacts")


class Spam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    marked_as_spam_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="spams")


class SpamLikelihood(db.Model):
    phone_number = db.Column(db.String(20), primary_key=True)
    spam_count = db.Column(db.Integer, nullable=False)


User.contacts = db.relationship("Contact", order_by=Contact.id, back_populates="user")
User.spams = db.relationship("Spam", order_by=Spam.id, back_populates="user")
