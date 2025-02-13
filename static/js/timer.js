// Ustaw czas sesji w sekundach (np. 5 minut)
const sessionTime = 10 * 60; // 5 minut w sekundach

// Sprawdź, czy czas pozostały jest już zapisany w sessionStorage
let timeLeft = sessionStorage.getItem('timeLeft') ? parseInt(sessionStorage.getItem('timeLeft')) : sessionTime;

// Funkcja do aktualizacji timera
function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;

    // Formatuj czas jako MM:SS
    const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    document.getElementById('countdown').textContent = formattedTime;

    // Sprawdź, czy czas się skończył
    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        alert("Sesja wygasła. Zostaniesz przekierowany do strony głównej.");
        // Usuń pozostały czas z sessionStorage
        sessionStorage.removeItem('timeLeft');
        // Możesz dodać kod do przekierowania
        window.location.href = '/'; // Przykład przekierowania
    } else {
        timeLeft--;
        // Zapisz pozostały czas w sessionStorage
        sessionStorage.setItem('timeLeft', timeLeft);
    }
}

function resetTimer() {
    sessionStorage.removeItem('timeLeft');
}

// Rozpocznij odliczanie
const timerInterval = setInterval(updateTimer, 1000);

// Początkowe wywołanie, aby natychmiast wyświetlić timer
updateTimer();