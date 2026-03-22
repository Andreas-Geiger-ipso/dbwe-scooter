from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    bookings = db.relationship("Booking", backref="user")

class Scooter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battery = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bookings = db.relationship("Booking", backref="scooter")

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scooter_id = db.Column(db.Integer, db.ForeignKey('scooter.id'), nullable=False)