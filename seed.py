from database import db, Movie, Showing, Coupon, User, Reservation, Ticket
from datetime import datetime, date
from app import app


def seed_db():
    
    tickets = [
        
        Ticket(
            type = "Bilet normalny",
            price = 30,
        ),
        
        Ticket(
            type = "Bilet ulgowy",
            price = 15,
        ),
        

    ]

    for ticket in tickets:
        db.session.add(ticket)
    
    
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
            image_url="https://pelnasala.pl/wp-content/uploads/2021/03/000AL6DUAHLIREO8-C125.jpg",
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
            show_time=datetime(2025, 1, 7, 20, 00),
            available_seats=30,
        ),
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
            lang_type="lektor",
            show_time=datetime(2025, 2, 1, 15, 00),
            available_seats=30,
        ),
        Showing(
            movie_id=1,
            movie_format="3D",
            lang_type="dubbing",
            show_time=datetime(2025, 2, 1, 20, 00),
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

    db.session.commit()  # Zapisz pokazy, aby uzyskać ich ID


    for showing in showings:
        showing.create_seats()

    coupons = [
        
        Coupon(
            coupon_id=1,
            coupon_code=1111,
            discount_value=10,
            expiration_date=datetime(2028,2,3,18,00),
            status="aktywny",
        )
    ]

    for coupon in coupons:
        db.session.add(coupon)

    
    users = [
        
        User(
            username = "admin",
            password = "admin",
        )
    ]

    for user in users:
        db.session.add(user)









    db.session.commit()
    


with app.app_context():
    db.create_all()
    seed_db()
