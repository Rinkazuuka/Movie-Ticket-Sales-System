document.getElementById('Wstecz').addEventListener('click', function() {
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

// akceptuj regulamin
document.getElementById('exampleCheck1').addEventListener('change', function() {
    var submitButton = document.getElementById('submitButton');
    submitButton.disabled = !this.checked;
});

// disabled bez kliknięcia
document.getElementById('submitButton').disabled = true;