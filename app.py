from flask import Flask, render_template, abort, flash, redirect, url_for
from database import db, Movie, Showing, Reservation, User, Coupon, Ticket, Seat
from datetime import date, datetime
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, session
import uuid
from flask import jsonify
import json

# zapisywanie pdf
from flask import Response, send_file
from io import BytesIO
from reportlab.pdfgen import canvas


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///your_database.db"  # Zmień na odpowiednią bazę danych
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.secret_key = "your_secret_key"  # Ustaw silny klucz sesji


@app.route("/")
def show_movies():
    movies = Movie.query.all()  # Pobierz wszystkie filmy
    return render_template("index.html", movies=movies)


@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()

    # Sprawdzenie, czy film istnieje
    if movie is None:
        abort(404)  # Zwróć błąd 404, jeśli film nie istnieje

    showings = Showing.query.filter_by(movie_id=movie_id)
    grouped_showings = defaultdict(list)
    for showing in showings:
        show_date = showing.show_time.date()
        grouped_showings[show_date].append(showing)

    # Przekazanie zgrupowanych seansów do szablonu
    return render_template(
        "movie.html",
        movie=movie,
        showings=showings,
        grouped_showings=grouped_showings,
        current_date=datetime.now().date(),
    )

    # return render_template("movie.html", movie=movie, showings=showings)



@app.route("/showing/<showing_id>")
def showing(showing_id):
    
    tickets = Ticket.query.all()
    showing = Showing.query.filter_by(showing_id=showing_id).first()
    seats = Seat.query.filter_by(showing_id=showing_id).all()
    if showing is None:
        abort(404)

    grouped_seats = defaultdict(list)
    for seat in seats:
        seat_row = seat.row
        grouped_seats[seat_row].append(seat)

    return render_template(
        "showing.html",
        showing=showing,
        tickets=tickets,
        seats=seats,
        grouped_seats=grouped_seats,
    )


@app.route("/showing/<showing_id>/personal")
def personal(showing_id):
    showing = Showing.query.filter_by(showing_id=showing_id).first()
    return render_template("personal.html", showing=showing)


@app.route("/showing/<showing_id>/personal/payment", methods=["GET", "POST"])
def payment(showing_id):

    if request.method == "POST":
        username = request.form.get("user-name")
        email = request.form.get("user-email")
        session["username"] = username
        session["email"] = email
        

        # losuj unikalny bilet
        session["ticket_number"] = str(uuid.uuid4())[:8]

        return redirect(url_for("payment", showing_id=showing_id))

    # GET
    showing = Showing.query.filter_by(showing_id=showing_id).first()
    username = session.get("username", "N/A")
    email = session.get("email", "N/A")
    return render_template(
        "payment.html", showing=showing, username=username, email=email
    )


@app.route("/check_coupon", methods=["POST"])
def check_coupon():
    coupon_code = request.form.get("coupon_code")

    # czy kupon jest w bazie
    coupon = Coupon.query.filter_by(coupon_code=coupon_code, status="aktywny").first()

    if coupon:
        # prawidłowy
        return jsonify({"valid": True, "discount": coupon.discount_value})
    else:
        # nieprawidłowy
        return jsonify({"valid": False, "discount": 0})



"""@app.route("/showing/<showing_id>/personal/payment/summary")
def summary(showing_id):
    showing = Showing.query.filter_by(showing_id=showing_id).first()

    # Pobranie informacji o użytkowniku z sesji
    username = session.get("username", "N/A")
    email = session.get("email", "N/A")
    ticketnumber = session.get("ticket_number", "Nie ma biletu")
    seatsordered = session.get("seats", [])
    print("Seats ordered:", seatsordered)

    # Dodanie rezerwacji do bazy po zapłaceniu
    new_reservation = Reservation(
        showing_id=showing_id,
        ticket_code=ticketnumber,
        number_of_tickets=len(seatsordered),
        username=username,
        email=email,
        status="ważny",
    )
    db.session.add(new_reservation)
    db.session.commit()

    # Aktualizacja miejsc w bazie
    for seat_info in seatsordered:
        row, place = seat_info
        seat = Seat.query.filter_by(showing_id=showing_id, row=row, place=place).first()
        if seat:
            seat.taken = True
            db.session.commit()

    # Przypisanie miejsc do rezerwacji
    for seat_info in seatsordered:
        row, place = seat_info
        reservation_seat = {
            'reservation_id': new_reservation.reservation_id,
            'row': row,
            'place': place
        }
        # Możesz dodać logikę zapisania do tabeli rezerwacji miejsc
        db.session.commit()

    # Pobranie rezerwacji z bazy
    reservation = Reservation.query.filter_by(
        reservation_id=new_reservation.reservation_id
    ).first()

    print("Seats Ordered:", seatsordered)

    return render_template("summary.html", 
                           showing=showing, 
                           reservation=reservation,
                           email=email,
                           seatsordered=seatsordered)"""

"""@app.route("/showing/<showing_id>/personal/payment/summary")
def summary(showing_id):
    showing = Showing.query.filter_by(showing_id=showing_id).first()

    # Pobranie informacji o użytkowniku z sesji
    username = session.get("username", "N/A")
    email = session.get("email", "N/A")
    ticketnumber = session.get("ticket_number", "Nie ma biletu")

    # Dodanie rezerwacji do bazy po zapłaceniu
    new_reservation = Reservation(
        showing_id=showing_id,
        ticket_code=ticketnumber,
        number_of_tickets=14,
        username=username,
        email=email,
        status="ważny",
    )
    db.session.add(new_reservation)
    db.session.commit()

    # Pobranie rezerwacji z bazy
    reservation = Reservation.query.filter_by(
        reservation_id=new_reservation.reservation_id
    ).first()

    return render_template("summary.html", 
                           showing=showing, 
                           reservation=reservation,
                           email=email)"""

@app.route("/showing/<showing_id>/personal/payment/summary")
def summary(showing_id):
    showing = Showing.query.filter_by(showing_id=showing_id).first()

    # Pobranie danych z sesji
    selected_seats = session.get('occupiedSeats', [])  # Domyślnie pusta lista, jeśli brak danych
    print("Zdeserializowane miejsca:", selected_seats)

    # Liczba biletów
    number_of_tickets = len(selected_seats)
    print("Ilość biletów:", number_of_tickets)

    # Pobranie informacji o użytkowniku z sesji
    username = session.get("username", "N/A")
    email = session.get("email", "N/A")
    ticketnumber = session.get("ticket_number", "Nie ma biletu")

    '''# Pobierz wybrane miejsca z sesji
    selected_seats = session.get('seats', "N/A")
    number_of_tickets = len(selected_seats)  # Liczba zarezerwowanych miejsc
    print("Ilosc biletów", number_of_tickets)'''

    '''# Pobierz wybrane miejsca z sesji i zdeserializuj je
    selected_seats = json.loads(session.get('occupiedSeats', "[]"))
    print("Zdeserializowane miejsca:", selected_seats)
    print(type(selected_seats))
    number_of_tickets = len(selected_seats)  # Liczba zarezerwowanych miejsc
    print("Ilosc biletów", number_of_tickets)

    # Przykład dostępu do poszczególnych elementów
    for seat in selected_seats:
        print(f"Rząd: {seat['row']}, Miejsce: {seat['place']}, Bilet: {seat['ticket_type']}")'''

    ###

    # Dodanie rezerwacji do bazy po zapłaceniu
    new_reservation = Reservation(
        showing_id=showing_id,
        ticket_code=ticketnumber,
        number_of_tickets=number_of_tickets,  # Zmieniona liczba biletów
        username=username,
        email=email,
        status="ważny",
    )
    db.session.add(new_reservation)
    db.session.commit()

    # Pobranie rezerwacji z bazy
    reservation = Reservation.query.filter_by(
        reservation_id=new_reservation.reservation_id
    ).first()


    return render_template("summary.html", 
                           showing=showing, 
                           reservation=reservation,
                           email=email,
                           number_of_tickets=number_of_tickets,
                           selected_seats = selected_seats)  # Przekazanie liczby biletów



# generowanie biletu pdf
def generate_pdf_file(reservation, showing, movie):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 750, "Bilet PopKino")

    # szczegóły rezerwacji
    p.drawString(100, 700, f"Imię i nazwisko: {reservation.username}")
    p.drawString(100, 675, f"Email: {reservation.email}")
    p.drawString(100, 650, f"Tytuł filmu: {movie.title}")
    p.drawString(
        100, 625, f"Data seansu: {showing.show_time.strftime('%Y-%m-%d %H:%M')}"
    )
    p.drawString(100, 600, f"Numer biletu: {reservation.ticket_code}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


# pobierz pdf
@app.route("/generate_pdf/<int:reservation_id>")
def generate_pdf(reservation_id):

    reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
    if not reservation:
        abort(404)

    showing = Showing.query.filter_by(showing_id=reservation.showing_id).first()
    movie = Movie.query.filter_by(movie_id=showing.movie_id).first()

    pdf_file = generate_pdf_file(reservation, showing, movie)
    return send_file(pdf_file, as_attachment=True, download_name="ticket.pdf")


# panel admina
@app.route("/admin", methods=["GET", "POST"])
def admin_view():
    if request.method == "POST":
        username = request.form.get("admin-user-name")
        password = request.form.get("admin-password")

        # czy usera mamy w bazie
        admin_user = User.query.filter_by(username=username, password=password).first()

        if admin_user:
            # zalogowany
            return redirect(url_for("check_tickets"))
        else:
            # Złe dane
            error_message = "Nieprawidłowy login lub hasło. Spróbuj ponownie."
            return render_template("admin.html", error=error_message)

    return render_template("admin.html")


# sprawdzamy czy bilet jest ważny
@app.route("/admin/bilety", methods=["GET", "POST"])
def check_tickets():
    if request.method == "POST":
        ticket_code = request.form.get("client-ticket-code")

        correct_ticket = Reservation.query.filter_by(
            ticket_code=ticket_code, status="ważny"
        ).first()

        if correct_ticket:
            # seans
            showing = Showing.query.filter_by(
                showing_id=correct_ticket.showing_id
            ).first()

            # jaki film
            movie = Movie.query.filter_by(movie_id=showing.movie_id).first()
            if movie is None:
                error_message = "Nie znaleziono filmu powiązanego z biletem."
                return render_template("tickets.html", error=error_message)

            # Pobierz miejsca zarezerwowane na ten pokaz NOWE
            reserved_seats = Seat.query.filter_by(
                showing_id=showing.showing_id, taken=True
            ).all()

            # Sformatuj dane miejsc dla szablonu
            reserved_seats_details = [
                {"row": seat.row, "place": seat.place} for seat in reserved_seats
            ]

            success_message = "Ten bilet jest prawidłowy"
            return render_template(
                "tickets.html",
                success=success_message,
                reservation=correct_ticket,
                showing=showing,
                movie=movie,
                reserved_seats=reserved_seats_details,  # Przekazanie miejsc do szablonu
            )

        else:
            error_message = "Nieprawidłowy bilet"
            return render_template("tickets.html", error=error_message)

    return render_template("tickets.html")


'''@app.route('/api/book_seats', methods=['POST'])
def book_seats():
    data = request.get_json()
    for seat_data in data:
        seat = Seat.query.filter_by(showing_id=seat_data['showing_id'], row=seat_data['row'], place=seat_data['place']).first()
        if seat:
            seat.taken = True  # Ustaw 'taken' na True
            db.session.commit()  # Zapisz zmiany w bazie danych
    return jsonify({'message': 'Seats booked successfully!'}), 200'''

@app.route('/api/book_seats', methods=['POST'])
def book_seats():
    # Pobranie danych z ciała żądania JSON
    data = request.get_json()
    print("Odebrane dane z fetch:", data)  # Debugowanie danych z frontendu

    # Zapisanie danych w sesji Flask
    session['occupiedSeats'] = data  # Zapisujemy całą listę miejsc w sesji
    print("Dane zapisane w sesji:", session['occupiedSeats'])

    # Przetwarzanie danych (zaznaczenie miejsc jako zajęte w bazie danych)
    for seat_data in data:
        seat = Seat.query.filter_by(showing_id=seat_data['showing_id'], row=seat_data['row'], place=seat_data['place']).first()
        if seat:
            seat.taken = True  # Ustaw 'taken' na True
            db.session.commit()  # Zapisz zmiany w bazie danych

    # Zwrócenie odpowiedzi JSON
    return jsonify({'message': 'Seats booked and saved to session successfully!'}), 200



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


with app.app_context():
    db.create_all()  # Tworzy wszystkie tabele

if __name__ == "__main__":
    app.run(debug=True)
