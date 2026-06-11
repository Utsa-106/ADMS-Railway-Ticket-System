from datetime import datetime
from uuid import uuid4

from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS

from database import get_db_connection


app = Flask(__name__)
app.secret_key = "railway-ticket-booking-secret"
CORS(app)


STATIONS = [
    "Dhaka",
    "Chattogram",
    "Rajshahi",
    "Khulna",
    "Sylhet",
    "Rangpur",
    "Mymensingh",
    "Cumilla",
]

TRAINS = [
    {
        "number": "704",
        "name": "Mahanagar Provati",
        "from": "Dhaka",
        "to": "Chattogram",
        "departure": "07:45",
        "arrival": "14:00",
        "classes": ["S_CHAIR", "SNIGDHA", "AC_S"],
    },
    {
        "number": "722",
        "name": "Subarna Express",
        "from": "Dhaka",
        "to": "Chattogram",
        "departure": "16:30",
        "arrival": "21:50",
        "classes": ["S_CHAIR", "SNIGDHA"],
    },
    {
        "number": "753",
        "name": "Silkcity Express",
        "from": "Dhaka",
        "to": "Rajshahi",
        "departure": "14:40",
        "arrival": "21:05",
        "classes": ["S_CHAIR", "SNIGDHA", "AC_S", "AC_B"],
    },
    {
        "number": "773",
        "name": "Kalni Express",
        "from": "Dhaka",
        "to": "Sylhet",
        "departure": "15:00",
        "arrival": "21:30",
        "classes": ["S_CHAIR", "SNIGDHA", "AC_S"],
    },
]

CLASS_FARES = {
    "S_CHAIR": 350,
    "SNIGDHA": 650,
    "AC_S": 900,
    "AC_B": 1200,
}

COACH_NAMES = ["KA", "KHA", "GA", "GHA"]
SEAT_NUMBERS = range(1, 9)
COACHES = [
    {
        "name": coach_name,
        "seats": [f"{coach_name}-{seat_number}" for seat_number in SEAT_NUMBERS],
    }
    for coach_name in COACH_NAMES
]
BOOKED_SEATS = {"KA-1", "KA-2", "GA-3", "GHA-4"}
MAX_TICKETS_PER_BOOKING = 4

SMART_ROUTE_PROFILES = {
    ("Dhaka", "Chattogram"): {"crowd": "High", "delay": "Medium", "tip": "Reach the station early and keep at least 30 minutes in hand before departure."},
    ("Dhaka", "Rajshahi"): {"crowd": "Medium", "delay": "Low", "tip": "Book early to get your preferred seat."},
    ("Dhaka", "Sylhet"): {"crowd": "Medium", "delay": "Medium", "tip": "Choose a comfortable class for a long journey if budget allows."},
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        stations=STATIONS,
        classes=CLASS_FARES.keys(),
        advisor_result=None,
    )


@app.route("/smart-trip-advisor", methods=["POST"])
def smart_trip_advisor():
    from_station = request.form["advisor_from"]
    to_station = request.form["advisor_to"]
    journey_date = request.form["advisor_date"]
    train_class = request.form["advisor_class"]

    advisor_result = build_trip_advice(from_station, to_station, journey_date, train_class)

    return render_template(
        "index.html",
        stations=STATIONS,
        classes=CLASS_FARES.keys(),
        advisor_result=advisor_result,
    )


@app.route("/seat-selection", methods=["POST"])
def seat_selection():
    booking = {
        "from_station": request.form["from"],
        "to_station": request.form["to"],
        "journey_date": request.form["journeyDate"],
        "train_class": request.form["class"],
        "phone": request.form["phone"],
    }

    if booking["from_station"] == booking["to_station"]:
        return render_template(
            "index.html",
            stations=STATIONS,
            classes=CLASS_FARES.keys(),
            error="Departure and destination station cannot be same.",
        )

    session["booking"] = booking
    trains = find_trains(booking)
    coaches = fetch_available_coaches(booking["from_station"], booking["to_station"])

    return render_template(
        "seat-selection.html",
        booking=booking,
        trains=trains,
        coaches=coaches,
        booked_seats=BOOKED_SEATS,
        fare=calculate_fare(booking["train_class"]),
    )


@app.route("/otp-verification", methods=["POST"])
def otp_verification():
    booking = session.get("booking")
    if not booking:
        return redirect(url_for("home"))

    selected_seats = [seat for seat in request.form.get("selected_seats", "").split(",") if seat]
    if not selected_seats:
        return "Please select at least one seat."

    if len(selected_seats) > MAX_TICKETS_PER_BOOKING:
        return "You can book maximum 4 tickets at a time."

    otp = request.form["otp"]
    if not verify_otp(otp):
        return "Invalid OTP. Demo OTP is 1234."

    per_seat_fare = calculate_fare(booking["train_class"])
    service_charge = 20
    booking.update(
        {
            "train": request.form["train"],
            "passenger_name": request.form["passenger_name"],
            "nid": request.form["nid"],
            "email": request.form.get("email", ""),
            "seats": selected_seats,
            "per_seat_fare": per_seat_fare,
            "service_charge": service_charge,
            "fare": per_seat_fare * len(selected_seats),
            "total": per_seat_fare * len(selected_seats) + service_charge,
        }
    )
    session["booking"] = booking
    return redirect(url_for("payment_details"))


@app.route("/payment-details", methods=["GET", "POST"])
def payment_details():
    booking = session.get("booking")
    if not booking:
        return redirect(url_for("home"))

    if request.method == "POST":
        payment_method = request.form["payment_method"]
        payment_number = request.form["payment_number"]
        process_payment(payment_method, payment_number, booking["total"])
        booking["payment_method"] = payment_method
        booking["payment_number"] = payment_number
        booking["payment_status"] = "PAID"
        booking["transaction_id"] = f"BR-{uuid4().hex[:10].upper()}"
        booking["issued_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
        session["booking"] = booking
        return redirect(url_for("ticket"))

    return render_template("payment-details.html", booking=booking)


@app.route("/ticket")
def ticket():
    booking = session.get("booking")
    if not booking or booking.get("payment_status") != "PAID":
        return redirect(url_for("home"))

    return render_template("ticket.html", booking=booking)


def find_trains(booking):
    matches = [
        train
        for train in TRAINS
        if train["from"] == booking["from_station"]
        and train["to"] == booking["to_station"]
        and booking["train_class"] in train["classes"]
    ]
    return matches or TRAINS[:2]


def calculate_fare(train_class):
    return CLASS_FARES.get(train_class, CLASS_FARES["S_CHAIR"])


def fetch_available_coaches(from_station, to_station):
    return COACHES


def verify_otp(otp):
    return otp == "1234"


def process_payment(payment_method, payment_number, fare):
    print(f"Processing {payment_method} payment of BDT {fare} from {payment_number}.")


def build_trip_advice(from_station, to_station, journey_date, train_class):
    profile = SMART_ROUTE_PROFILES.get(
        (from_station, to_station),
        {"crowd": "Low", "delay": "Low", "tip": "Normal demand is expected, but early booking is still recommended."},
    )

    try:
        travel_day = datetime.strptime(journey_date, "%Y-%m-%d").strftime("%A")
    except ValueError:
        travel_day = "Selected day"

    class_note = "Lower fare option" if train_class == "S_CHAIR" else "Comfort-focused option"

    return {
        "route": f"{from_station} to {to_station}",
        "date": journey_date,
        "day": travel_day,
        "class": train_class,
        "class_note": class_note,
        "crowd": profile["crowd"],
        "delay": profile["delay"],
        "tip": profile["tip"],
    }


import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
