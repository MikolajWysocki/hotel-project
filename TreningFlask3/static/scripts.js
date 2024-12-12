// Pobieranie przycisków
const calculatePriceButton = document.getElementById("calculate-price");
const makeReservationButton = document.getElementById("make-reservation");

// Funkcja do obliczania ceny
calculatePriceButton.addEventListener("click", () => {
    const formData = getFormData();
    if (!formData) return;

    // Obliczanie liczby dni
    const diffInTime = new Date(formData.czas_koniec) - new Date(formData.czas_start);
    const diffInDays = diffInTime / (1000 * 60 * 60 * 24); // Zamiana ms na dni

    // Obliczanie ceny
    const pricePerNight = formData.room_type === 1 ? 100 : 150;
    const totalPrice = diffInDays * pricePerNight;

    // Wyświetlanie ceny
    const priceDisplay = document.getElementById("price-display");
    priceDisplay.innerHTML = `
        <h3>Reservation Summary</h3>
        <p>Guest: ${formData.guest_name}, Age: ${formData.guest_age}</p>
        <p>Room Type: ${formData.room_type === 1 ? "Single (1 Person)" : "Double (2 Persons)"}</p>
        <p>Stay Duration: ${diffInDays} night(s)</p>
        <p>Total Price: <strong>${totalPrice} zł</strong></p>
    `;
});

// Funkcja do wysyłania danych w formacie JSON
makeReservationButton.addEventListener("click", async () => {
    const formData = getFormData();
    if (!formData) return;

    // Pakowanie danych w JSON
    const reservationData = {
        guest_name: formData.guest_name,
        guest_age: formData.guest_age,
        room_type: formData.room_type,
        czas_start: formData.czas_start,
        czas_koniec: formData.czas_koniec,
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/api/reservations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(reservationData),
        });

        if (response.ok) {
            alert("Reservation made successfully!");
        } else {
            alert("Failed to make reservation.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while making the reservation.");
    }
});

// Funkcja do pobierania danych z formularza
function getFormData() {
    const formData = new FormData(document.getElementById("reservation-form"));
    const guestName = formData.get("guest_name");
    const guestAge = parseInt(formData.get("guest_age"), 10);
    const roomType = parseInt(formData.get("room_type"), 10);
    const startDate = formData.get("czas_start");
    const endDate = formData.get("czas_koniec");

    if (!guestName || !guestAge || !roomType || !startDate || !endDate) {
        alert("Please fill out all fields!");
        return null;
    }

    if (new Date(startDate) >= new Date(endDate)) {
        alert("End date must be after start date!");
        return null;
    }

    return { guest_name: guestName, guest_age: guestAge, room_type: roomType, czas_start: startDate, czas_koniec: endDate };
}