// Function to handle form submission
document.getElementById('railForm').addEventListener('submit', function(e) {
    // Prevent the page from reloading
    e.preventDefault();

    // Get input values from the form
    const trainName = document.getElementById('name').value;
    const trainRoute = document.getElementById('route').value;
    const rawTime = document.getElementById('time').value;

    // Convert 24-hour time to 12-hour AM/PM format using built-in function
    // This makes the time display 
    const timeObject = new Date('2026-01-01T' + rawTime);
    const finalTime = timeObject.toLocaleString('en-US', { 
        hour: 'numeric', 
        minute: 'numeric', 
        hour12: true 
    });

    // Create a new table row for the data
    const tableBody = document.getElementById('list');
    const row = `
        <tr>
            <td>${trainName}</td>
            <td>${trainRoute}</td>
            <td>${finalTime}</td>
        </tr>
    `;

    // Add the new row to the table
    tableBody.innerHTML += row;

    // Reset the form fields for next entry
    this.reset();
});