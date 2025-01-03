from flask import Flask, render_template
from database import db, Movie, Showing
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Zmień na odpowiednią bazę danych
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


    
@app.route('/')
def show_movies():
    movies = Movie.query.all()  # Pobierz wszystkie filmy
    return render_template('index.html', movies=movies)


@app.route('/movie/<movie_id>')
def movie_details(movie_id=1):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    showings = Showing.query.filter_by(movie_id=movie_id)
    return render_template('movie.html', movie=movie, showings=showings)

@app.route('/showing/<showing_id>')
def showing(showing_id):
    showing = Showing.query.filter_by(showing_id=showing_id).first()
    return render_template('showing.html', showing=showing)



with app.app_context():
    db.create_all()  # Tworzy wszystkie tabele
    # new_user = Movie(title='Vaiana 2', description='Vaiana wraz z nowymi kompanami wyrusza w podróż po dalekich wodach Oceanii, by odszukać inne ludzkie plemiona.', duration=120, release_date=date(2001, 12, 30), image_url="https://fwcdn.pl/fpo/81/30/10048130/8139711.3.jpg")
    # db.session.add(new_user)
    # db.session.commit()

    # showing = Showing(movie_id=1, movie_format="2D", lang_type="dubbing", show_time=datetime(2025, 2, 1, 18, 00), available_seats=30)
    # db.session.add(showing)
    # db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
        
