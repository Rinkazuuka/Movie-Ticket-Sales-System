# System rezerwacji biletów w kinie

Celem naszego projektu było stworzenie aplikacji webowej, która umożliwia rezerwację biletów na seanse kinowe oraz zewnętrznego systemu do elektronicznej weryfikacji biletów. W realizacji tego zadania wykorzystaliśmy technologie takie jak **HTML, CSS, biblioteka Bootstrap, JavaScript, Python, jQuery oraz Flask.**

Główne funkcje naszej aplikacji to:
* rezerwacja miejsca na interaktywnej mapie kina
* wybór rodzaju dodanych biletów
* formularz do danych kontaktowych
* dodawanie kuponu rabatowego
* bilet elektroniczny w wersji PDF
* weryfikacja ważności blietu przez admina
* cadcedcwacsc


## Otwieranie projektu
#### 1. Zainstaluj potrzebne biblioteki z pliku *requirements.txt*
Użyj komendy `pip3 install -r requirements.txt`

    Flask==2.2.5
    Flask-sqlalchemy==3.1.1
    Werkzeug==2.2.2
    Flask-WTF
    /kino-rezerwacje
    email_validator
    reportlab==4.0.0
    

#### 2. Stwórz wirtualne środowisko
W terminalu utwórz środowisko za pomocą komendy `python3 -m venv .env`. Po stworzeniu wirtualnego środowiska aktywuj go komendą `.\.env\Scripts\activate`

#### 3. Uruchom plik *seed.py*
Aby stworzyć bazę danych potrzebną do działania aplikacji oraz wypełnić ją przykładowymi danymi, otwórz plik *seed.py* za pomocą komendy `python seed.py`

#### 4. Uruchom program *app.py*
Uruchom program *app.py* za pomocą komendy `python -m flask run`

## Organizacja plików
    │ 
    ├── /instance                     # Bazy danych
    │   └── database                  
    │ 
    ├── /static                       # Pliki statyczne (CSS, JS, obrazy)
    │   └── css/                      # Pliki css
    │       └── styles.css            
    │   ├── images/                   # Obrazy 
    │   └── js/                       # Pliki js
    │       ├── coupon.js             # Javascript do kupona rabatowego
    │       ├── timer.js              # Javascript do licznika czasu
    │       └── script.js             # Javascript do całego projektu
    │ 
    ├── /templates                    # Szablony HTML
    │   ├── 404.html                  # Strona 404
    │   ├── admin.html                # Strona logowania dla admina
    │   ├── base_reservation.html     # Podstawowy szablon do widoku rezerwacji
    │   ├── base_website.html         # Podstawowy szablon do widoku aplikacji
    │   ├── footer.html               # Stopka
    │   ├── head.html                 # Zagłówek stron
    │   ├── index.html                # Strona główna
    │   ├── logo.html                 # Logo
    │   ├── movie.html                # Strona z opisem wybranego filmu
    │   ├── personal.html             # Widok danych osobowych przy rezerwacji
    │   ├── payment.html              # Widok płatności przy rezerwacji
    │   ├── showing.html              # Widok wyboru miejsc i biletów
    │   ├── summary.html              # Podsumowanie zakupu biletu
    │   └── tickets.html              # Strona do sprawdzania biletów przez admina
    │
    ├── .gitignore             
    ├── database.py                   # Skrypt do klas w bazie danych
    ├── requirements.txt              # Wymagane biblioteki
    └── seed.py                       # Skrypt do inicjalizacji bazy danych



## Interfejs API
Aplikacja udostępnia kilka punktów końcowych API, które umożliwiają interakcję z systemem rezerwacji. Aplikacja zawiera endpointy takie jak:

* `/` - Strona główna aplikacji 
* `/movie/<int:movie_id>` - Opis filmu z bazy danych
* `/showing/<showing_id>/personal` - Rezerwacja miejsc na wybrany seans
* `/showing/<showing_id>/personal/payment` - Płatność za wybrane bilety
* `/showing/<showing_id>/personal/payment/summary` - Podsumowanie transakcji 
* `/check_coupon` - Sprawdzanie, czy kupon istnieje
* `/generate_pdf/<int:reservation_id>` - Generowanie biletu w formacie PDF
* `/admin` - Logowanie do konta admina
* `/admin/bilety`- Strona do weryfikacji biletów przez admina

## Bazy danych
Baza danych jest zbudowana przy użyciu SQL-Alchemy i zawiera następujące tabele:
* `movies` - baza z dostępnymi filmami
* `showings` - baza z dostępnymi seansami na filmy
* `reservations` - baza z dokonanymi rezerwacjami na seanse
* `user` - baza dla zarejestrowanych użytkowników
* `coupons` - baza dostępnych kuponów rabatowych
* `seats` - baza z miejscami siedzącymi w kinie
* `tickets` - baza z dostępnymi biletami do wyboru

### Movies
Tabela reprezentuje filmy, które są dostępne dla użytkowników.

    class Movie(db.Model):
        __tablename__ = "movies"
        
        movie_id = db.Column(db.Integer, primary_key=True)               # ID filmu
        title = db.Column(db.String(255), nullable=False)                # Tytuł filmu
        description = db.Column(db.Text, nullable=True)                  # Opis filmu 
        duration = db.Column(db.Integer, nullable=False)                 # Czas trwania filmu
        release_date = db.Column(db.Date, nullable=False)                # Data produkcji
        image_url = db.Column(db.String, nullable=True)                  # URL do okładki filmu
        created_at = db.Column(db.DateTime, default=datetime.utcnow)     # Data utworzenia
    
        showings = db.relationship("Showing", back_populates="movie")    # Relacja z tabelą Showing

### Showings
Tabela reprezentuje pokazy filmowe w kinie, które są dostępne dla użytkowników.

    class Showing(db.Model):
        __tablename__ = "showings"
    
        showing_id = db.Column(db.Integer, primary_key=True)                                        # ID pokazu
        movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"), nullable=False)          # ID filmu
        movie_format = db.Column(db.String(10), nullable=False)                                     # 2D/3D
        lang_type = db.Column(db.String(20), nullable=False)                                        # dubbing/napisy/lektor
        show_time = db.Column(db.DateTime, nullable=False)                                          # Data pokazu
    
        movie = db.relationship("Movie", back_populates="showings")

### Reservations
Tabela reprezentuje seanse filmowe, które są dostępne dla użytkowników.

    class Reservation(db.Model):
        __tablename__ = 'reservations'
        
        reservation_id = db.Column(db.Integer, primary_key=True)                                    # ID rezerwacji
        ticket_code = db.Column(db.String, nullable=False)                                          # Kod biletu
        showing_id = db.Column(db.Integer, db.ForeignKey('showings.showing_id'), nullable=False)    # ID pokazu
        number_of_tickets = db.Column(db.Integer, nullable=False)                                   # Liczba biletów
        reservation_date = db.Column(db.DateTime, default=datetime.utcnow)                          # Data rezerwacji
        status = db.Column(db.String(20), nullable=False)                                           # "ważny", "nieważny"
        created_at = db.Column(db.DateTime, default=datetime.utcnow)                                # Data utworzenia
        username = db.Column(db.String(100), nullable=False)                                        #
        email = db.Column(db.String(100), nullable=False)

### User
Tabela reprezentuje użytkowników personelu kina wraz z ich danymi do logowania. W swoim projekcie nie zaimplementowałyśmy żadnych zabezpieczeń do logowania, gdyż chciałyśmy tylko przetestować działanie weryfikacji biletów.

    class User(db.Model):
        username = db.Column(db.String, primary_key=True)   # Nazwa użytkownika
        password = db.Column(db.String, nullable=False)     # Hasło użytkownika

### Tickets
Tabela przechowywująca możliwe typy biletów (np. bilet normalny, bilet ulgowy)

    class Ticket(db.Model):
        type = db.Column(db.String, primary_key=True)       # Nazwa typu biletu (normalny, ulgowy)
        price = db.Column(db.Integer, nullable=False)       # Cena biletu

### Seats
Tabela z miejscami na wybrane filmy.

    class Seat(db.Model):
        __tablename__ = 'seats'
        
        seat_id = db.Column(db.Integer, primary_key=True)                                                 # ID siedzenia
        showing_id =  db.Column(db.Integer, db.ForeignKey("showings.showing_id"), nullable=False)         # ID pokazu
        row = db.Column(db.Integer, nullable=False)                                                       # rząd
        place = db.Column(db.Integer, nullable=False)                                                     # miejsce
        taken = db.Column(db.Boolean, nullable=False, default=False)                                      # zajęte/wolne
    
        showing = db.relationship("Showing", back_populates="seats")                                      # relacja z tabelą Showing


# Główne widoki i funkcjonalności w aplikacji

### Widok strony głównej
Strona główna, która wyświetla się po uruchomieniu aplikacji
![image](https://github.com/user-attachments/assets/722ef405-06f8-478d-af3e-82c80e004067)

### Widok filmu

Po wybraniu filmu, który nas interesuje trafiamy na taki widok, gdzie możemy dowiedzieć się kiedy są najbliższe seanse i kupić bilet
![image](https://github.com/user-attachments/assets/ee8eed2c-99c3-447c-ac60-b4147f695b90)

### Widok rezerwacji miejsc

Następnie możemy wybrać miejsca, które nas interesują oraz ulgę, jeżeli ją posiadamy. System automatycznie wyliczy nam cenę.
![image](https://github.com/user-attachments/assets/63e1ec18-4e93-48c1-a605-7aafb3036c09)

### Widok podsumowania

Podsumowanie z naszego wyboru siedzeń oraz miejsce na wpisanie swoich danych osobowych i akceptację regulaminu
![image](https://github.com/user-attachments/assets/368a285d-808b-4fc5-b6c6-0902e597d054)

### Widok płatności

To tutaj mozemy zobaczyć podsumowanie naszej rezerwacji, miejsce na kupon rabatowy, koszt naszej rezeracji oraz możemy wybrać sposób płatności, który nas interesuje
![image](https://github.com/user-attachments/assets/814e05e2-5b86-4345-b580-3662a7747f5a)

### Finalizacja zakupu

To tutaj otrzymujemy nasz kod biletu, który możemy pobrać
![image](https://github.com/user-attachments/assets/9aab0bf0-eae7-4d51-861b-470004774509)

### Widok logowania do panelu admina 

### Widok weryfikacji biletów przez admina


### Strona 404
Strona 404 wyświetla się, gdy serwer nie może znaleźć żądanego zasobu.

![image](https://github.com/user-attachments/assets/c0eed2a8-6806-43d5-b0c3-48c94753ee1c)

