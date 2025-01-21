# System rezerwacji biletów w kinie

Celem naszego projektu było stworzenie aplikacji webowej, która umożliwia rezerwację biletów na seanse kinowe oraz zewnętrznego systemu do elektronicznej weryfikacji biletów. W realizacji tego zadania wykorzystaliśmy technologie takie jak HTML, CSS, biblioteka Bootstrap, JavaScript, Python, jQuery oraz Flask.

Główne funkcje naszej aplikacji, zawartość:
* cdc
* ccfd


## Otwieranie projektu
### 1. Zainstaluj potrzebne biblioteki z pliku *requirements.txt*
Użyj komendy `pip3 install -r requirements.txt`

![image](https://github.com/user-attachments/assets/50f6e756-9c38-462f-bc69-a5e06fa7c58a)

### 2. Stwórz wirtualne środowisko
W terminalu utwórz środowisko za pomocą komendy `python3 -m venv .env`. Po stworzeniu wirtualnego środowiska aktywuj go komendą `.\.env\Scripts\activate`

![image](https://github.com/user-attachments/assets/7213a705-7315-413e-8b8d-0c3c96b16c87)

### 3. Uruchom plik *seed.py*
Aby stworzyć bazę danych potrzebną do działania aplikacji oraz wypełnić ją przykładowymi danymi, otwórz plik *seed.py* za pomocą komendy `python seed.py`

![image](https://github.com/user-attachments/assets/0b121cc5-8b29-496d-8550-be4c78514153)

### 4. Uruchom program
Uruchom program za pomocą komendy `python -m flask run`

## Organizacja plików
![image](https://github.com/user-attachments/assets/733f442f-6e11-4395-95fd-20ed71dd54b8)



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


// dokumentację interfejsu API — szczegółowy opis endpointów, metod, parametrów żądań i odpowiedzi, jeśli aplikacja udostępnia API;

## Bazy danych
Baza danych jest zbudowana przy użyciu SQL-Alchemy i zawiera następujące tabele:
* movies
* showings
* reservations
* user
* coupons

// opis schematów baz danych, relacji między nimi i tym podobnych;

## Podstawowa ścieżka przejścia aplikacji
przewodniki dla końcowych użytkowników wyjaśniające działanie różnych funkcji i modułów aplikacji;


![image](https://github.com/user-attachments/assets/c0eed2a8-6806-43d5-b0c3-48c94753ee1c)

