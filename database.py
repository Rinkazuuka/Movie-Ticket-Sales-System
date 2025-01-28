from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import Set
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    release_date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    # direction= db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    showings = db.relationship("Showing", back_populates="movie")


class Showing(db.Model):
    __tablename__ = "showings"

    showing_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"), nullable=False)
    # screen_id = db.Column(db.Integer, db.ForeignKey('screens.screen_id'), nullable=False)
    movie_format = db.Column(db.String(10), nullable=False)  # 2D/3D
    lang_type = db.Column(db.String(20), nullable=False)  # dubbing/napisy/lektor
    show_time = db.Column(db.DateTime, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

    movie = db.relationship("Movie", back_populates="showings")
    seats = db.relationship("Seat", back_populates="showing")  # Dodaj tę linię

    def create_seats(self):
        for row in range(1, 7):  # 6 rzędów
            for place in range(1, 11):  # 10 miejsc w każdym rzędzie
                seat = Seat(row=row, place=place, showing_id=self.showing_id)  # Upewnij się, że showing_id jest poprawnie przypisane
                db.session.add(seat)
        db.session.commit()

class Reservation(db.Model):
    __tablename__ = 'reservations'
    reservation_id = db.Column(db.Integer, primary_key=True)
    ticket_code = db.Column(db.String, nullable=False)
    showing_id = db.Column(db.Integer, db.ForeignKey('showings.showing_id'), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)  # "ważny", "nieważny"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    place = db.Column(db.Integer, nullable=False)
    ticket_type = db.Column(db.String(100), nullable=False)



class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    
class Ticket(db.Model):
    type = db.Column(db.String, primary_key=True)
    price = db.Column(db.Integer, nullable=False)


class Seat(db.Model):
    __tablename__ = 'seats'
    
    seat_id = db.Column(db.Integer, primary_key=True)
    showing_id =  db.Column(db.Integer, db.ForeignKey("showings.showing_id"), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    place = db.Column(db.Integer, nullable=False)
    taken = db.Column(db.Boolean, nullable=False, default=False)
    ticket_type = db.Column(db.String, nullable=True, default='Bilet normalny')

    showing = db.relationship("Showing", back_populates="seats")  # Dodaj tę linię


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

class Coupon(db.Model):
    __tablename__ = 'coupons'

    coupon_id = db.Column(db.Integer, primary_key=True)
    coupon_code = db.Column(db.String(50), unique=True, nullable=False)
    discount_value = db.Column(db.Float, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # "aktywny", "nieaktywny"
