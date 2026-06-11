const selectedSeats = new Set();
const maxTickets = 4;
const selectedSeatsInput = document.getElementById("selectedSeats");
const seatPreview = document.getElementById("seatPreview");
const bookingForm = document.getElementById("bookingForm");

document.querySelectorAll(".seat:not(.booked)").forEach((seatButton) => {
    seatButton.addEventListener("click", () => {
        const seat = seatButton.dataset.seat;

        if (selectedSeats.has(seat)) {
            selectedSeats.delete(seat);
            seatButton.classList.remove("selected");
        } else {
            if (selectedSeats.size >= maxTickets) {
                alert("You can book maximum 4 tickets at a time.");
                return;
            }

            selectedSeats.add(seat);
            seatButton.classList.add("selected");
        }

        const seats = Array.from(selectedSeats);
        selectedSeatsInput.value = seats.join(",");
        seatPreview.textContent = seats.length ? seats.join(", ") : "None";
    });
});

bookingForm?.addEventListener("submit", (event) => {
    if (!selectedSeatsInput.value) {
        event.preventDefault();
        alert("Please select at least one seat.");
        return;
    }

    if (selectedSeats.size > maxTickets) {
        event.preventDefault();
        alert("You can book maximum 4 tickets at a time.");
    }
});
