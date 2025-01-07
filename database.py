from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import Set
from sqlalchemy.orm import relationship


db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'
    
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    release_date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    # direction= db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    showings = db.relationship('Showing', back_populates='movie')


# class Screen(db.Model):
#     __tablename__ = 'screens'
    
#     screen_id = db.Column(db.Integer, primary_key=True)
#     screen_number = db.Column(db.String(50), nullable=False)
#     capacity = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Showing(db.Model):
    __tablename__ = 'showings'
    
    showing_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    # screen_id = db.Column(db.Integer, db.ForeignKey('screens.screen_id'), nullable=False)
    movie_format = db.Column(db.String(10), nullable=False)  # 2D/3D
    lang_type = db.Column(db.String(20), nullable=False)  # dubbing/napisy/lektor
    show_time = db.Column(db.DateTime, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

    movie = db.relationship('Movie', back_populates='showings')

    # movie = relationship('Movie', foreign_keys='Showing.movie_id')
    # showing = relationship('Movie', foreign_keys='Showing.showing_id')

# class Reservation(db.Model):
#     __tablename__ = 'reservations'
    
#     reservation_id = db.Column(db.Integer, primary_key=True)
#     showing_id = db.Column(db.Integer, db.ForeignKey('showings.showing_id'), nullable=False)
#     number_of_tickets = db.Column(db.Integer, nullable=False)
#     reservation_date = db.Column(db.DateTime, default=datetime.utcnow)
#     status = db.Column(db.String(20), nullable=False)  # "zrealizowana", "anulowana"
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     username = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)

# class Payment(db.Model):
#     __tablename__ = 'payments'
    
#     payment_id = db.Column(db.Integer, primary_key=True)
#     reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.reservation_id'), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     payment_date = db.Column(db.DateTime, default=datetime.utcnow)
#     payment_method = db.Column(db.String(20), nullable=False)  # "karta", "przelew"
#     status = db.Column(db.String(20), nullable=False)  # "zrealizowana", "nieudana"
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# class Coupon(db.Model):
#     __tablename__ = 'coupons'
    
#     coupon_id = db.Column(db.Integer, primary_key=True)
#     coupon_code = db.Column(db.String(50), unique=True, nullable=False)
#     discount_value = db.Column(db.Float, nullable=False)
#     expiration_date = db.Column(db.Date, nullable=False)
#     status = db.Column(db.String(20), nullable=False)  # "aktywny", "nieaktywny"

