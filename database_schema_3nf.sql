CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    nid VARCHAR(30) NOT NULL UNIQUE,
    email VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE stations (
    station_id SERIAL PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE trains (
    train_id SERIAL PRIMARY KEY,
    train_number VARCHAR(20) NOT NULL UNIQUE,
    train_name VARCHAR(100) NOT NULL
);

CREATE TABLE train_classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE train_routes (
    route_id SERIAL PRIMARY KEY,
    train_id INTEGER NOT NULL REFERENCES trains(train_id),
    from_station_id INTEGER NOT NULL REFERENCES stations(station_id),
    to_station_id INTEGER NOT NULL REFERENCES stations(station_id),
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    CONSTRAINT different_route_stations CHECK (from_station_id <> to_station_id)
);

CREATE TABLE class_fares (
    fare_id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL REFERENCES train_routes(route_id),
    class_id INTEGER NOT NULL REFERENCES train_classes(class_id),
    fare_amount NUMERIC(10, 2) NOT NULL CHECK (fare_amount >= 0),
    UNIQUE (route_id, class_id)
);

CREATE TABLE seats (
    seat_id SERIAL PRIMARY KEY,
    train_id INTEGER NOT NULL REFERENCES trains(train_id),
    class_id INTEGER NOT NULL REFERENCES train_classes(class_id),
    seat_number VARCHAR(10) NOT NULL,
    UNIQUE (train_id, seat_number)
);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    route_id INTEGER NOT NULL REFERENCES train_routes(route_id),
    class_id INTEGER NOT NULL REFERENCES train_classes(class_id),
    journey_date DATE NOT NULL,
    service_charge NUMERIC(10, 2) NOT NULL DEFAULT 20,
    booking_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE booking_seats (
    booking_seat_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    seat_id INTEGER NOT NULL REFERENCES seats(seat_id),
    seat_fare NUMERIC(10, 2) NOT NULL CHECK (seat_fare >= 0),
    UNIQUE (booking_id, seat_id)
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL UNIQUE REFERENCES bookings(booking_id) ON DELETE CASCADE,
    payment_method VARCHAR(30) NOT NULL,
    payment_number VARCHAR(50) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    paid_at TIMESTAMP
);

INSERT INTO stations (station_name) VALUES
('Dhaka'),
('Chattogram'),
('Rajshahi'),
('Khulna'),
('Sylhet'),
('Rangpur'),
('Mymensingh'),
('Cumilla');

INSERT INTO train_classes (class_name) VALUES
('S_CHAIR'),
('SNIGDHA'),
('AC_S'),
('AC_B');

INSERT INTO trains (train_number, train_name) VALUES
('704', 'Mahanagar Provati'),
('722', 'Subarna Express'),
('753', 'Silkcity Express'),
('773', 'Kalni Express');
