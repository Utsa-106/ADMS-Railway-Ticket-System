let selectedSeats = [];
const AC_PRICE = 1000;
const NON_AC_PRICE = 500;

window.onload = () => {
    refreshUI();
};

function refreshUI() {
    refreshSeatUI();
    renderAdminTable();
    renderUserHistory();
}

function refreshSeatUI() {
    const acGrid = document.getElementById('ac-grid');
    const nonAcGrid = document.getElementById('non-ac-grid');
    acGrid.innerHTML = '';
    nonAcGrid.innerHTML = '';
    
    const bookings = JSON.parse(localStorage.getItem('railway_db')) || [];
    const allBookedSeats = bookings.flatMap(b => b.seats.split(', '));

    for (let i = 1; i <= 8; i++) createSeat(acGrid, i, "AC-", AC_PRICE, allBookedSeats);
    for (let i = 9; i <= 16; i++) createSeat(nonAcGrid, i, "N-", NON_AC_PRICE, allBookedSeats);
}

function createSeat(container, num, prefix, price, allBookedSeats) {
    const seatId = prefix + num;
    const seat = document.createElement('div');
    seat.className = 'seat-box';
    seat.innerText = seatId;

    if (allBookedSeats.includes(seatId)) seat.classList.add('booked');

    seat.onclick = () => {
        if (seat.classList.contains('booked')) return;
        if (seat.classList.contains('selected')) {
            seat.classList.remove('selected');
            selectedSeats = selectedSeats.filter(s => s.id !== seatId);
        } else if (selectedSeats.length < 4) {
            seat.classList.add('selected');
            selectedSeats.push({ id: seatId, fare: price });
        } else {
            alert("Limit: 4 seats.");
        }
        updateSummary();
    };
    container.appendChild(seat);
}

function updateSummary() {
    const total = selectedSeats.reduce((sum, s) => sum + s.fare, 0);
    document.getElementById('display-seats').innerText = selectedSeats.map(s => s.id).join(', ') || "None";
    document.getElementById('display-price').innerText = total;
}

document.getElementById('ticket-form').onsubmit = function(e) {
    e.preventDefault();
    if (selectedSeats.length === 0) return alert("Select seats!");

    const name = document.getElementById('p-name').value;
    const route = document.getElementById('p-train').value;
    const fare = document.getElementById('display-price').innerText;
    const seats = document.getElementById('display-seats').innerText;

    const bookings = JSON.parse(localStorage.getItem('railway_db')) || [];
    bookings.push({ name, route, fare, seats, id: Date.now() }); // Unique ID for deleting
    localStorage.setItem('railway_db', JSON.stringify(bookings));

    document.getElementById('t-name').innerText = name;
    document.getElementById('t-train').innerText = route;
    document.getElementById('t-seats').innerText = seats;
    document.getElementById('t-fare').innerText = fare;
    document.getElementById('ticket-modal').style.display = "flex";
};

// DELETE FUNCTION
function deleteBooking(id) {
    if (confirm("Are you sure you want to delete this record?")) {
        let bookings = JSON.parse(localStorage.getItem('railway_db')) || [];
        bookings = bookings.filter(b => b.id !== id);
        localStorage.setItem('railway_db', JSON.stringify(bookings));
        refreshUI();
    }
}

function renderAdminTable() {
    const dbData = JSON.parse(localStorage.getItem('railway_db')) || [];
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = ''; 
    dbData.forEach(item => {
        tableBody.innerHTML += `<tr>
            <td>${item.name}</td><td>${item.route}</td>
            <td>${item.seats}</td><td>${item.fare} TK</td>
            <td><button class="del-btn" onclick="deleteBooking(${item.id})">Delete</button></td>
        </tr>`;
    });
}

function renderUserHistory() {
    const dbData = JSON.parse(localStorage.getItem('railway_db')) || [];
    const historyDiv = document.getElementById('user-history');
    if (dbData.length === 0) {
        historyDiv.innerHTML = '<p style="font-size: 12px; color: #888;">No recent bookings.</p>';
        return;
    }
    historyDiv.innerHTML = dbData.slice(-3).map(item => `
        <div class="history-item">
            <strong>${item.name}</strong> - ${item.seats} (${item.fare} TK)
        </div>
    `).join('');
}

function closeTicket() {
    document.getElementById('ticket-modal').style.display = "none";
    document.getElementById('ticket-form').reset();
    selectedSeats = [];
    updateSummary();
    refreshUI();
}

function openAdmin() { if (prompt("Password:") === "123") document.getElementById('admin-panel').style.display = "flex"; }
function closeAdmin() { document.getElementById('admin-panel').style.display = "none"; }