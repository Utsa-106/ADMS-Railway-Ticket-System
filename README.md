# 🚂 Online Railway Ticket Booking System with Check Trip Feature

A full-stack web-based railway ticket-booking demo developed for the **Advanced Database Management Systems Lab (CSE-468)**.

The project follows the general online ticket-booking process of Bangladesh Railway. It allows users to search for trains, select seats, verify passenger information using a demo OTP, choose a payment method, and generate a printable e-ticket.

The project also introduces a new passenger-support feature called **Check Trip**, which displays estimated crowd level, delay risk, and journey advice before booking.

> **Disclaimer:** This is an academic prototype and is not an official Bangladesh Railway application. The interface and booking flow are inspired by the general online railway ticketing process.

---

## 🖥️ Project UI Showcase

|                                                        🏠 Homepage                                                       |                                                        💺 Seat Selection                                                       |                                                        🎫 E-Ticket                                                       |
| :----------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------: |
| <img width="500" alt="Homepage" src="https://github.com/user-attachments/assets/625c4114-6af3-4069-a24c-a1053997f7ae" /> | <img width="500" alt="Seat Selection" src="https://github.com/user-attachments/assets/862e056c-5270-4f2d-ae1b-eee384909cd6" /> | <img width="500" alt="E-Ticket" src="https://github.com/user-attachments/assets/ffddc367-ca21-422f-a0f1-a993f889cf68" /> |
|                                        `index.html` — Train Search and Check Trip                                        |                                        `seat-selection.html` — Train and Seat Selection                                        |                                      `ticket.html` — Printable Booking Confirmation                                      |

---

## ✨ Main Features

* Train search by departure station, destination station, journey date, and seat class
* Same departure and destination validation
* Matching train display with schedule and fare information
* Interactive coach-based seat-selection system
* Available, selected, and booked seat indicators
* Maximum four-seat booking limit
* Passenger information collection
* Demo OTP verification using code `1234`
* Payment options: bKash, Nagad, Rocket, and Card
* Automatic fare and service-charge calculation
* Unique transaction ID generation
* Printable e-ticket generation
* Responsive user interface
* Check Trip feature for journey guidance

---

## 🧭 Check Trip Feature

Check Trip is the main new feature of this project.

Before booking, users can select:

* Departure station
* Destination station
* Journey date
* Seat class

The system then displays:

* Selected route
* Journey date
* Estimated crowd level
* Estimated delay risk
* Journey advice

Currently, Check Trip uses predefined route profiles. In the future, it can be connected with real-time or historical railway data to provide more accurate journey information.

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

### Backend

* Python
* Flask
* Flask Session
* Flask-CORS

### Database

* PostgreSQL
* psycopg2
* Third Normal Form (3NF) Database Design
* Neon PostgreSQL Cloud

### Development and Deployment

* GitHub
* Render
* UUID for transaction ID generation
* VS Code

---

## 🗃️ Database Design

The database schema is designed using **Third Normal Form (3NF)** to reduce data duplication and improve data integrity.

Main tables include:

* Users
* Stations
* Trains
* Train Routes
* Train Classes
* Class Fares
* Seats
* Bookings
* Booking Seats
* Payments

The schema is available in:

```text
database_schema_3nf.sql
```

---

## 📁 Project Structure

```text
Online-Railway-Ticket-Booking-System
│
├── app.py
├── database.py
├── database_schema_3nf.sql
├── requirements.txt
│
├── templates
│   ├── index.html
│   ├── seat-selection.html
│   ├── payment-details.html
│   └── ticket.html
│
└── static
    ├── styles.css
    └── script.js
```

---

## 🔄 Booking Workflow

```text
Search Train
    ↓
Select Train and Seats
    ↓
Enter Passenger Information
    ↓
Verify Demo OTP
    ↓
Select Payment Method
    ↓
Generate Printable E-Ticket
```

---


---

## 🧪 Demo Information

### Demo OTP

```text
1234
```

### Payment

Payment processing is simulated. No real financial transaction is performed.

---

## ⚠️ Current Limitations

* OTP uses a fixed demo code
* No real SMS is sent
* Payment processing is simulated
* Booked seats are predefined
* Seat availability does not update after every booking
* Check Trip uses predefined data
* User registration and login are not included

---

## 🔮 Future Improvements

* Real SMS OTP integration
* Real payment gateway integration
* Live seat availability updates
* User registration and booking history
* Admin dashboard
* Real-time or historical data for Check Trip
* QR code integration for e-ticket verification
* Email booking confirmation

---

## 📄 License

This project was developed for academic and educational purposes.
