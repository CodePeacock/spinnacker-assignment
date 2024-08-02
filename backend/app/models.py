from __init__ import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    city = db.Column(db.String(128), nullable=True)
    country = db.Column(db.String(128), nullable=True)
    verified = db.Column(db.Boolean, default=False)


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
