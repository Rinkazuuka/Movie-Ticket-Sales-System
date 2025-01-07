from database import db, Movie, Showing
from datetime import datetime, date
from app import app


def seed_db():
    movies = [
        Movie(
            title="Vaiana 2",
            description="Vaiana wraz z nowymi kompanami wyrusza w podróż po dalekich wodach Oceanii, by odszukać inne ludzkie plemiona.",
            duration=100,
            release_date=date(2024, 11, 28),
            image_url="https://fwcdn.pl/fpo/81/30/10048130/8139711.3.jpg",
        ),
        Movie(
            title="Coco",
            description="Dwunastoletni meksykański chłopiec imieniem Miguel usiłuje zgłębić tajemnice rodzinnej legendy.",
            duration=105,
            release_date=date(2017, 10, 27),
            image_url="https://m.media-amazon.com/images/M/MV5BMDIyM2E2NTAtMzlhNy00ZGUxLWI1NjgtZDY5MzhiMDc5NGU3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        ),
        Movie(
            title="Co w duszy gra",
            description="Joe Gardner prowadzi zespół muzyczny w gimnazjum. Jego prawdziwą pasją jest jednak jazz. Joe przeżywa kryzys - zaczyna zadawać sobie pytania: Po co tu jestem? Jaki jest cel mojego życia?",
            duration=106,
            release_date=date(2020, 3, 5),
            image_url="https://static.wikia.nocookie.net/pixar/images/4/46/Co_w_duszy_gra_poster_2.jpg/revision/latest?cb=20200314201141&path-prefix=pl",
        ),
        Movie(
            title="Naprzód",
            description="Dwóch braci próbuje sprowadzić na ziemię drugą połowę ciała swojego ojca, gdyż nieudane czary powodują, że pojawia się tylko od pasa w dół.",
            duration=102,
            release_date=date(2020, 3, 6),
            image_url="https://images-3.rakuten.tv/storage/global-movie/translation/artwork/cb369d07-78dd-4238-904a-65e556244cb6-naprzod-1611406746.jpeg",
        ),
    ]

    for movie in movies:
        db.session.add(movie)

    showings = [
        Showing(
            movie_id=1,
            movie_format="2D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 12, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=1,
            movie_format="2D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 18, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=1,
            movie_format="2D",
            lang_type="napisy",
            show_time=datetime(2025, 2, 3, 15, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=1,
            movie_format="3D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 3, 18, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=2,
            movie_format="2D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 12, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=2,
            movie_format="2D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 18, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=2,
            movie_format="2D",
            lang_type="napisy",
            show_time=datetime(2025, 2, 3, 15, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=2,
            movie_format="3D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 3, 18, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=3,
            movie_format="2D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 12, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=3,
            movie_format="2D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 18, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=3,
            movie_format="2D",
            lang_type="napisy",
            show_time=datetime(2025, 2, 3, 15, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=3,
            movie_format="3D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 3, 18, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=4,
            movie_format="2D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 12, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=4,
            movie_format="2D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 18, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=4,
            movie_format="2D",
            lang_type="napisy",
            show_time=datetime(2025, 2, 3, 15, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=4,
            movie_format="3D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 3, 18, 00),
            available_seats=30,
        ),
    ]

    for showing in showings:
        db.session.add(showing)

    db.session.commit()


with app.app_context():
    db.create_all()
    seed_db()
