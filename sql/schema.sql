-- CINEMAX MOVIE BOOKING SYSTEM
-- Database schema
-- Compatible with app.py and the three project triggers.

CREATE DATABASE IF NOT EXISTS movie_booking;
USE movie_booking;

-- Movies displayed by movies.html
-- app.py uses:
--   m[1] = movie_name
--   m[5] = screen
--   m[6] = rating
-- and selects dates_available by movie_name.
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(150) NOT NULL UNIQUE,
    language VARCHAR(50) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    dates_available VARCHAR(500) NOT NULL,
    screen VARCHAR(50) NOT NULL,
    rating DECIMAL(2,1) NOT NULL
);

-- Theatre choices are displayed using data[0][1:].
-- Keep the first column as city and the remaining columns as theatre names.
CREATE TABLE IF NOT EXISTS theatre_area (
    city VARCHAR(50) PRIMARY KEY,
    theatre_1 VARCHAR(100) NOT NULL,
    theatre_2 VARCHAR(100),
    theatre_3 VARCHAR(100),
    theatre_4 VARCHAR(100)
);

-- Timeslot choices are displayed using data[0][1:].
-- The first column is the screen identifier.
CREATE TABLE IF NOT EXISTS timeslot (
    screen VARCHAR(50) PRIMARY KEY,
    slot_1 VARCHAR(20) NOT NULL,
    slot_2 VARCHAR(20) NOT NULL,
    slot_3 VARCHAR(20) NOT NULL,
    slot_4 VARCHAR(20)
);

-- Stores the selected movie/theatre/screen/date/time combination.
CREATE TABLE IF NOT EXISTS movieshow_config (
    config_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(150) NOT NULL,
    theatre_code VARCHAR(100) NOT NULL,
    screencode VARCHAR(50) NOT NULL,
    show_id VARCHAR(300) NOT NULL,
    show_date DATE NOT NULL,
    timeslot VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_show_id (show_id),
    INDEX idx_movie_date (movie_name, show_date)
);

-- Seat rows and their prices.
-- app.py reads row_config and later SELECTs price by row_id.
CREATE TABLE IF NOT EXISTS row_config (
    row_id VARCHAR(10) PRIMARY KEY,
    price INT NOT NULL
);

-- Individual seat numbers.
-- seats.html uses s[0] as the seat number.
CREATE TABLE IF NOT EXISTS seat_config (
    seat_no VARCHAR(10) PRIMARY KEY
);

-- Seats booked for a particular show.
-- Names match prevent_double_booking trigger exactly:
-- show_id, row_id, seat_no.
CREATE TABLE IF NOT EXISTS seat_booking (
    seat_booking_id INT AUTO_INCREMENT PRIMARY KEY,
    phno VARCHAR(20) NOT NULL,
    show_id VARCHAR(300) NOT NULL,
    row_id VARCHAR(10) NOT NULL,
    seat_no VARCHAR(10) NOT NULL,
    price INT NOT NULL,
    booking_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    booking_id VARCHAR(20) NOT NULL,
    INDEX idx_seat_show (show_id, row_id, seat_no),
    INDEX idx_booking_id (booking_id)
);

-- Food/snack catalogue.
-- app.py expects:
-- s[0] = sno
-- s[1] = snack item
-- s[2] = price
CREATE TABLE IF NOT EXISTS foodbev_config (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    snack_item VARCHAR(100) NOT NULL,
    price INT NOT NULL
);

-- Snacks attached to a booking.
CREATE TABLE IF NOT EXISTS snack_booking (
    snack_booking_id INT AUTO_INCREMENT PRIMARY KEY,
    phno VARCHAR(20) NOT NULL,
    show_id VARCHAR(300) NOT NULL,
    snack_no INT NOT NULL,
    snack_item VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    amount INT NOT NULL,
    booking_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    booking_id VARCHAR(20) NOT NULL,
    INDEX idx_snack_booking_id (booking_id),
    INDEX idx_snack_show (show_id)
);

-- Payment record.
-- update_payment_total trigger uses booking_id and writes total_amount.
CREATE TABLE IF NOT EXISTS payment_details (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    phno VARCHAR(20) NOT NULL,
    show_id VARCHAR(300) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    total_amount INT NOT NULL DEFAULT 0,
    booking_id VARCHAR(20) NOT NULL,
    payment_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_payment_booking_id (booking_id)
);

-- Booking audit log.
-- log_booking trigger inserts only booking_id.
CREATE TABLE IF NOT EXISTS booking_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id VARCHAR(20) NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_log_booking_id (booking_id)
);
