let totalRevenue = 0;
let totalTickets = 0;
let selectedSeats = [];

// Generate AC Seats (1-8)
const acGrid = document.getElementById('ac-grid');
for (let i = 1; i <= 8; i++) createSeat(acGrid, i, "AC-", 1000);

// Generate Non-AC Seats (9-16)
const nonAcGrid = document.getElementById('non-ac-grid');
for (let i = 9; i <= 16; i++) createSeat(nonAcGrid, i, "N-", 500);

function createSeat(container, num, prefix, price) {
    let seat = document.createElement('div');
    seat.className = 'seat-box';
    seat.innerText = prefix + num;
    
    seat.onclick = () => {
        if (seat.classList.contains('booked')) return;
        
        if (seat.classList.contains('selected')) {
            seat.classList.remove('selected');
            selectedSeats = selectedSeats.filter(s => s.id !== prefix + num);
        } else if (selectedSeats.length < 4) {
            seat.classList.add('selected');
            selectedSeats.push({ id: prefix + num, fare: price });
        } else {
            alert("Maximum limit: 4 seats per booking.");
        }
        updateUI();
    };
    container.appendChild(seat);
}

function updateUI() {
    let total = selectedSeats.reduce((sum, s) => sum + s.fare, 0);
    document.getElementById('display-seats').innerText = selectedSeats.map(s => s.id).join(', ') || "None";
    document.getElementById('display-price').innerText = total;
}

document.getElementById('ticket-form').onsubmit = function(e) {
    e.preventDefault();
    if (selectedSeats.length === 0) return alert("Please select at least one seat.");

    let name = document.getElementById('p-name').value;
    let journey = document.getElementById('p-train').value;
    let fare = document.getElementById('display-price').innerText;
    let seats = document.getElementById('display-seats').innerText;

    // 1. Show Digital Ticket to Passenger
    document.getElementById('t-name').innerText = name;
    document.getElementById('t-train').innerText = journey;
    document.getElementById('t-seats').innerText = seats;
    document.getElementById('t-fare').innerText = fare;
    document.getElementById('ticket-modal').style.display = "flex";

    // 2. Add to Admin Records
    document.getElementById('table-body').innerHTML += `<tr>
        <td>${name}</td><td>${journey}</td><td>${seats}</td><td>${fare} TK</td>
        <td><button class="del-btn" onclick="cancelBooking(this, ${fare}, ${selectedSeats.length})">Cancel</button></td>
    </tr>`;

    // 3. Mark seats as Booked
    document.querySelectorAll('.seat-box.selected').forEach(s => {
        s.classList.remove('selected');
        s.classList.add('booked');
    });

    // 4. Update Admin Stats
    totalRevenue += parseInt(fare);
    totalTickets += selectedSeats.length;
    document.getElementById('rev').innerText = totalRevenue;
    document.getElementById('sold').innerText = totalTickets;

    selectedSeats = [];
    updateUI();
    this.reset();
};

function cancelBooking(btn, amount, count) {
    btn.parentElement.parentElement.remove();
    totalRevenue -= amount;
    totalTickets -= count;
    document.getElementById('rev').innerText = totalRevenue;
    document.getElementById('sold').innerText = totalTickets;
}

function closeTicket() { document.getElementById('ticket-modal').style.display = "none"; }
function openAdmin() { if (prompt("Admin Password:") === "123") document.getElementById('admin-panel').style.display = "block"; }