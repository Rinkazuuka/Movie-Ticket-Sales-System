document.getElementById('Wstecz').addEventListener('click', function () {
    // Cofnij do poprzedniej strony
    window.history.back();
});

function submitForm() {
    var form = document.getElementById('paymentForm');
    if (form.checkValidity()) {
        form.submit(); // Wysyła formularz, jeśli walidacja się powiedzie
    } else {
        // Jeśli walidacja się nie powiedzie, wyświetl komunikaty o błędach
        form.reportValidity();
    }
}


function updateSeat(index, ticketPrice, ticketType) {
    let seats = JSON.parse(sessionStorage.getItem('seats')) || [];

if (index >= 0 && index < seats.length) {
    seats[index].ticket_type = ticketType;
    seats[index].ticket_price = ticketPrice;
    sessionStorage.setItem('seats', JSON.stringify(seats));

    // Zapisz wybraną opcję w sessionStorage
    sessionStorage.setItem(`selectedTicketType_${seats[index].row}_${seats[index].place}`, ticketType);
    sessionStorage.setItem(`selectedTicketPrice_${seats[index].row}_${seats[index].place}`, ticketPrice);

    // Uaktualnij widok i sumę
    renderSelectedSeats(); // Renderuj ponownie wybrane miejsca
    calculateTotal(); // Przelicz całkowity koszt
}
}


function restoreSelectedSeats() {
    const seats = JSON.parse(sessionStorage.getItem('seats')) || [];

    seats.forEach(seat => {
        // Znajdź odpowiedni element w DOM
        const seatElement = document.querySelector(`.seat-card[data-row="${seat.row}"][data-place="${seat.place}"]`);
        if (seatElement) {
            seatElement.classList.add('selected'); // Dodaj klasę 'selected'
        }
    });
}


function checkIfAnySeatIsSelected() {
    console.log("checkIfAnySeatIsSelected")
    const seats = JSON.parse(sessionStorage.getItem('seats')) || [];
    const button = document.getElementById('Przejdz_dalej');

    if (seats.length > 0) {
        button.classList.remove('disabled');
        button.removeAttribute('disabled');
    } else {
        button.classList.add('disabled');
        button.setAttribute('disabled', 'true');
    }

    // Zawsze zachowaj klasę btn-primary, CSS będzie sterował wyglądem
    button.classList.add('btn-primary');
}


// Wybór miejsca
function toggleSeat(seatElement, row, place) {
    let seats = JSON.parse(sessionStorage.getItem('seats')) || [];
    console.log("Aktualna lista miejsc przed zapisaniem: ", seats);  // Logowanie przed dodaniem

    // Przełącz klasę 'selected' na klikniętym elemencie
    seatElement.classList.toggle('selected');
    const isSelected = seatElement.classList.contains('selected'); // Sprawdź, czy siedzenie jest zaznaczone

    // Sprawdź, czy siedzenie już istnieje w tablicy
    const seatIndex = seats.findIndex(seat => seat.row === row && seat.place === place);

    if (isSelected) {
        // Jeśli siedzenie jest zaznaczone, dodaj je do tablicy
        if (seatIndex === -1) {
            seats.push({
                row: row,
                place: place,
                selected: true,
                ticket_type: 'Bilet normalny',
                ticket_price: 30,
            });
        }
    } else {
        // Jeśli siedzenie nie jest zaznaczone, usuń je z tablicy
        if (seatIndex !== -1) {
            sessionStorage.removeItem(`selectedTicketType_${seats[seatIndex].row}_${seats[seatIndex].place}`);
            sessionStorage.removeItem(`selectedTicketPrice_${seats[seatIndex].row}_${seats[seatIndex].place}`);
            
            seats.splice(seatIndex, 1);
        }
    }

    // Logowanie po zaktualizowaniu listy miejsc
    console.log("Zaktualizowana lista miejsc: ", seats);
    sessionStorage.setItem('seats', JSON.stringify(seats));
    //console.log("Zaktualizowana lista miejsc po dodaniu do sesji", seats);
    console.log("Sesja po zapisaniu:", sessionStorage.getItem('seats'));
    renderSelectedSeats(); // Jeśli masz funkcję do renderowania zaznaczonych miejsc
    calculateTotal();
    checkIfAnySeatIsSelected(); // Sprawdź, czy odblokować przycisk

}

// Usuwanie za pomocą krzyżyka
function deleteSeat(index) {
    let seats = JSON.parse(sessionStorage.getItem('seats')) || [];

    // Znajdź miejsce, które ma być usunięte
    const seatToRemove = seats[index];

    sessionStorage.removeItem(`selectedTicketType_${seats[index].row}_${seats[index].place}`);
    sessionStorage.removeItem(`selectedTicketPrice_${seats[index].row}_${seats[index].place}`);

    // Usuń miejsce z tablicy
    seats.splice(index, 1);

    // Zaktualizuj sessionStorage
    sessionStorage.setItem('seats', JSON.stringify(seats));

    // Znajdź odpowiedni element w DOM i usuń klasę 'selected'
    const seatElement = document.querySelector(`.seat-card[data-row="${seatToRemove.row}"][data-place="${seatToRemove.place}"]`);
    if (seatElement) {
        seatElement.classList.remove('selected'); // Usuń klasę 'selected'
    }

    // Renderuj ponownie zaznaczone miejsca
    renderSelectedSeats();
    calculateTotal();
    checkIfAnySeatIsSelected();


}


function calculateTotal() {
    let total = 0;
    let seats = JSON.parse(sessionStorage.getItem('seats')) || [];
    seats.forEach(seat => {
        const price = parseFloat(seat.ticket_price);
        if (!isNaN(price)) {
            total += price;
        }
    });

    document.getElementById('totalAmount').innerText = total.toFixed(2);

}

function calculateTotalDiscount(discount = 0) {
    let total = 0;
    let seats = JSON.parse(sessionStorage.getItem('seats')) || [];
    seats.forEach(seat => {
        const price = parseFloat(seat.ticket_price);
        if (!isNaN(price)) {
            total += price;
        }
    });

    // Uwzględnienie rabatu
    const discountedTotal = Math.max(total - discount, 0); // Zapobiega ujemnej kwocie
    document.getElementById('totalAmountDiscount').innerText = discountedTotal.toFixed(2);
}

$(document).ready(function () {
    $("#coupon-form").on("submit", function (event) {
        event.preventDefault(); 

        var coupon_code = $("#discount-code").val(); // pobierz kupon z formularza

        $.ajax({
            url: "/check_coupon",  
            method: "POST",
            data: {
                coupon_code: coupon_code  
            },
            success: function (response) {
                if (response.valid) {
                    // Kod działa, zastosuj rabat
                    $("#discount-value").text("-" + response.discount + " zł");

                    // Ponowne obliczenie z rabatem
                    calculateTotalDiscount(response.discount);
                } else {
                    // Kod nie działa, brak rabatu
                    $("#discount-value").text("Brak rabatu");

                    // Obliczenie bez rabatu
                    calculateTotalDiscount();
                }
            },
            error: function () {
                alert("Wystąpił błąd podczas sprawdzania kodu rabatowego.");
            }
        });
    });

    // Pierwsze obliczenie bez rabatu po załadowaniu strony
    calculateTotalDiscount();
});

function updateTicketType(index, ticketType) {
    let seats = JSON.parse(sessionStorage.getItem('seats')) || [];
    if (seats[index]) {
        seats[index].ticketType = ticketType; // Zaktualizuj typ biletu
        sessionStorage.setItem('seats', JSON.stringify(seats));
        calculateTotal(); // Uaktualnij sumę po zmianie typu biletu
    }
}


