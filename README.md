# System rezerwacji biletów w kinie

Celem naszego projektu było stworzenie aplikacji webowej, która umożliwia rezerwację biletów na seanse kinowe oraz zewnętrznego systemu do elektronicznej weryfikacji biletów. W realizacji tego zadania wykorzystaliśmy technologie takie jak HTML, CSS, biblioteka Bootstrap, JavaScript, Python, jQuery oraz Flask.

Główne funkcje naszej aplikacji, zawartość:
* cdc
* ccfd


## Otwieranie projektu
### 1. Zainstaluj potrzebne biblioteki z pliku *requirements.txt*
Użyj komendy `pip3 install -r requirements.txt`

    Flask==2.2.5
    Flask-sqlalchemy==3.1.1
    Werkzeug==2.2.2
    Flask-WTF
    /kino-rezerwacje
    email_validator
    reportlab==4.0.0
    

### 2. Stwórz wirtualne środowisko
W terminalu utwórz środowisko za pomocą komendy `python3 -m venv .env`. Po stworzeniu wirtualnego środowiska aktywuj go komendą `.\.env\Scripts\activate`

![image](https://github.com/user-attachments/assets/7213a705-7315-413e-8b8d-0c3c96b16c87)

### 3. Uruchom plik *seed.py*
Aby stworzyć bazę danych potrzebną do działania aplikacji oraz wypełnić ją przykładowymi danymi, otwórz plik *seed.py* za pomocą komendy `python seed.py`

![image](https://github.com/user-attachments/assets/0b121cc5-8b29-496d-8550-be4c78514153)

### 4. Uruchom program
Uruchom program za pomocą komendy `python -m flask run`

## Organizacja plików
    │ 
    ├── /instance                 # Szablony HTML
    │   └── database              # Inicjalizacja aplikacji
    │ 
    ├── /static                   # Pliki statyczne (CSS, JS, obrazy)
    │   ├── css/                  # Inicjalizacja aplikacji
    │   ├── images/               # Modele bazy danych
    │   └── js/                   # Szablony HTML
    │       ├── base.html         # Szablon bazowy
    │       ├── index.html        # Strona główna
    │       ├── booking.html      # Strona rezerwacji
    │       └── confirmation.html # Strona potwierdzenia
    │ 
    ├── /templates                # Szablony HTML
    │   ├── 404.html              # Inicjalizacja aplikacji
    │   ├── admin.html            # Definicje tras (routes)
    │   ├── base_reservation.html # Modele bazy danych
    │   ├── base_website.html     # Inicjalizacja aplikacji
    │   ├── footer.html           # Definicje tras (routes)
    │   ├── head.html             # Modele bazy danych
    │   ├── index.html            # Inicjalizacja aplikacji
    │   ├── logo.html             # Definicje tras (routes)
    │   ├── movie.html            # Modele bazy danych
    │   ├── personal.html         # Modele bazy danych
    │   ├── showing.html          # Inicjalizacja aplikacji
    │   ├── summary.html          # Definicje tras (routes)
    │   └── tickets.html          # Formularze
    │
    ├── .gitignore             
    ├── database.py               # Skrypt do klas w bazie danych
    ├── requirements.txt          # Wymagane biblioteki
    └── seed.py                   # Skrypt do inicjalizacji bazy danych



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

