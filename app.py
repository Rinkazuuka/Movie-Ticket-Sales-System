from flask import Flask, render_template
from database import db, Movie, Showing
from datetime import date, datetime
from collections import defaultdict


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///your_database.db"  # Zmień na odpowiednią bazę danych
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def show_movies():
    movies = Movie.query.all()  # Pobierz wszystkie filmy
    return render_template("index.html", movies=movies)


@app.route("/movie/<movie_id>")
def movie_details(movie_id=1):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
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
    return render_template("showing.html", showing=showing)


with app.app_context():
    db.create_all()  # Tworzy wszystkie tabele

if __name__ == "__main__":
    app.run(debug=True)
