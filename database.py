import psycopg2


def get_db_connection():
    return psycopg2.connect(
        host="ep-sparkling-meadow-aq4gxlf0-pooler.c-8.us-east-1.aws.neon.tech",
        database="Railway-Ticketing-System",
        user="neondb_owner",
        password="npg_J7Fzb1qeYpjL",
        port="5432",
        sslmode="require",
    )


def register_user(full_name, phone, nid, email=None, password=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (full_name, phone, nid, email, password)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING user_id, full_name, phone, nid, email
        """,
        (full_name, phone, nid, email, password),
    )
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return user


def login_user(phone, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT user_id, full_name, phone, nid, email
        FROM users
        WHERE phone = %s AND password = %s
        """,
        (phone, password),
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def get_stations():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT station_id, station_name FROM stations ORDER BY station_name")
    stations = cur.fetchall()
    cur.close()
    conn.close()
    return stations


def get_train_classes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT class_id, class_name FROM train_classes ORDER BY class_id")
    classes = cur.fetchall()
    cur.close()
    conn.close()
    return classes


def search_train_routes(from_station, to_station, class_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            tr.route_id,
            t.train_id,
            t.train_number,
            t.train_name,
            tr.departure_time,
            tr.arrival_time,
            tc.class_id,
            tc.class_name,
            cf.fare_amount
        FROM train_routes tr
        JOIN trains t ON tr.train_id = t.train_id
        JOIN stations fs ON tr.from_station_id = fs.station_id
        JOIN stations ts ON tr.to_station_id = ts.station_id
        JOIN class_fares cf ON tr.route_id = cf.route_id
        JOIN train_classes tc ON cf.class_id = tc.class_id
        WHERE fs.station_name = %s
          AND ts.station_name = %s
          AND tc.class_name = %s
        ORDER BY tr.departure_time
        """,
        (from_station, to_station, class_name),
    )
    routes = cur.fetchall()
    cur.close()
    conn.close()
    return routes


def fetch_available_seats(train_id, class_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT seat_id, seat_number
        FROM seats
        WHERE train_id = %s AND class_id = %s
        ORDER BY seat_number
        """,
        (train_id, class_id),
    )
    seats = cur.fetchall()
    cur.close()
    conn.close()
    return seats


def create_booking(user_id, route_id, class_id, journey_date, service_charge=20):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO bookings (user_id, route_id, class_id, journey_date, service_charge)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING booking_id, user_id, route_id, class_id, journey_date, booking_status
        """,
        (user_id, route_id, class_id, journey_date, service_charge),
    )
    booking = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return booking


def add_booking_seat(booking_id, seat_id, seat_fare):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO booking_seats (booking_id, seat_id, seat_fare)
        VALUES (%s, %s, %s)
        RETURNING booking_seat_id, booking_id, seat_id, seat_fare
        """,
        (booking_id, seat_id, seat_fare),
    )
    booking_seat = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return booking_seat


def create_payment(booking_id, payment_method, payment_number, amount):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO payments (booking_id, payment_method, payment_number, amount, payment_status, paid_at)
        VALUES (%s, %s, %s, %s, 'PAID', CURRENT_TIMESTAMP)
        RETURNING payment_id, booking_id, amount, payment_status, paid_at
        """,
        (booking_id, payment_method, payment_number, amount),
    )
    payment = cur.fetchone()
    cur.execute(
        """
        UPDATE bookings
        SET booking_status = 'CONFIRMED'
        WHERE booking_id = %s
        """,
        (booking_id,),
    )
    conn.commit()
    cur.close()
    conn.close()
    return payment
