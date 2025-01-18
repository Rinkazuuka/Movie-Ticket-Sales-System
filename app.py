from flask import Flask, render_template, abort
from database import db, Movie, Showing, Reservation, User
from datetime import date, datetime
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, session
import uuid

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
    showing = Showing.query.filter_by(showing_id=showing_id).first()

    if showing is None:
        abort(404)  
        
    return render_template("showing.html", showing=showing)

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

        # Generowanie biletu
        session["ticket_number"] = str(uuid.uuid4())[:8]

        return redirect(url_for("payment", showing_id=showing_id))
    # Obsługa GET
    showing = Showing.query.filter_by(showing_id=showing_id).first()
    username = session.get("username", "N/A")
    email = session.get("email", "N/A")
    return render_template("payment.html", showing=showing, username=username, email=email)


@app.route("/showing/<showing_id>/personal/payment/summary")
def summary(showing_id):
    showing = Showing.query.filter_by(showing_id=showing_id).first()

    username = session.get("username", "N/A")
    email = session.get("email", "N/A")
    ticketnumber = session.get("ticket_number", "Nie ma biletu")

    # Dodaj rezerwację do bazy danych
    new_reservation = Reservation(
        showing_id=showing_id,
        ticket_code = ticketnumber,
        number_of_tickets=14,  # Możesz to dostosować w zależności od formularza
        username= username,
        email= email,
        status="ważny"
    )
    db.session.add(new_reservation)
    db.session.commit()

    reservation = Reservation.query.filter_by(reservation_id=new_reservation.reservation_id).first()


    return render_template(
        "summary.html",
        showing=showing,
        reservation=reservation
    )


# Sprawdzanie biletów
"""@app.route("/admin", methods=["GET", "POST"])
def admin_view():
    if request.method == "POST":
        return render_template("admin.html")
    
    return render_template(
        "admin.html"
    )
"""
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

@app.route("/admin/bilety", methods=["GET", "POST"])
def check_tickets():
    if request.method == "POST":
        ticket_code = request.form.get("client-ticket-code")

        correct_ticket = Reservation.query.filter_by(ticket_code=ticket_code, status = "ważny").first()

        if correct_ticket:
            # seans
            showing = Showing.query.filter_by(showing_id=correct_ticket.showing_id).first()
            # jaki film
            movie = Movie.query.filter_by(movie_id=showing.movie_id).first()
            if movie is None:
                error_message = "Nie znaleziono filmu powiązanego z biletem."
                return render_template("tickets.html", error=error_message)

            success_message = "Ten bilet jest prawidłowy"
            return render_template(
                "tickets.html",
                success = success_message,
                reservation=correct_ticket,
                showing=showing,
                movie=movie)
        
        else:
            error_message = "Nieprawidłowy bilet"
            return render_template("tickets.html", error=error_message)
    
    return render_template("tickets.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


with app.app_context():
    db.create_all()  # Tworzy wszystkie tabele

if __name__ == "__main__":
    app.run(debug=True)

