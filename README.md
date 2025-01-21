# System rezerwacji biletów w kinie

Celem naszego projektu było stworzenie aplikacji webowej, która umożliwia rezerwację biletów na seanse kinowe oraz zewnętrznego systemu do elektronicznej weryfikacji biletów. W realizacji tego zadania wykorzystaliśmy technologie takie jak HTML, CSS, biblioteka Bootstrap, JavaScript, Python, jQuery oraz Flask.

Główne funkcje naszej aplikacji, zawartość:
* cdc
* ccfd


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

#### 4. Uruchom program
Uruchom program za pomocą komendy `python -m flask run`

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

### Movies

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    release_date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    # direction= db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    showings = db.relationship("Showing", back_populates="movie")


## Podstawowa ścieżka przejścia aplikacji
przewodniki dla końcowych użytkowników wyjaśniające działanie różnych funkcji i modułów aplikacji;


![image](https://github.com/user-attachments/assets/c0eed2a8-6806-43d5-b0c3-48c94753ee1c)

