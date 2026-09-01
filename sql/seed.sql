-- CINEMAX MOVIE BOOKING SYSTEM
-- Corrected seed data for the uploaded movie posters.
-- Run schema.sql first.

USE movie_booking;

-- movie_name matches the poster title used by movies.html:
-- static/images/<movie_name>.jpg

INSERT INTO movies
(movie_name, language, genre, dates_available, screen, rating)
VALUES
    ('Antony', 'Malayalam', 'Action/Drama', '2026-09-05,2026-09-06,2026-09-07,2026-09-08', 'SCREEN-1', 6.5),
    ('Atharva', 'Telugu', 'Action/Crime', '2026-09-05,2026-09-06,2026-09-07,2026-09-08', 'SCREEN-2', 6.5),
    ('Hi Nanna', 'Telugu', 'Romance/Drama', '2026-09-05,2026-09-06,2026-09-07,2026-09-08', 'SCREEN-3', 8.2),
    ('Joram', 'Hindi', 'Drama/Thriller', '2026-09-05,2026-09-06,2026-09-07', 'SCREEN-1', 7.5),
    ('96', 'Tamil', 'Romance/Drama', '2026-09-06,2026-09-07,2026-09-08', 'SCREEN-2', 8.5),
    ('Operation Valentine', 'Telugu', 'Action/Drama', '2026-09-05,2026-09-06,2026-09-07,2026-09-08', 'SCREEN-3', 5.2),
    ('Philips', 'Malayalam', 'Comedy/Drama', '2026-09-06,2026-09-07,2026-09-08', 'SCREEN-1', 7.0),
    ('Silent Night', 'English', 'Action/Thriller', '2026-09-05,2026-09-06,2026-09-07', 'SCREEN-2', 5.3),
    ('The Bikeriders', 'English', 'Crime/Drama', '2026-09-05,2026-09-06,2026-09-07,2026-09-08', 'SCREEN-3', 6.8),
    ('Wonka', 'English', 'Fantasy/Musical', '2026-09-05,2026-09-06,2026-09-07,2026-09-08', 'SCREEN-1', 7.0)
ON DUPLICATE KEY UPDATE
    language = VALUES(language),
    genre = VALUES(genre),
    dates_available = VALUES(dates_available),
    screen = VALUES(screen),
    rating = VALUES(rating);

INSERT INTO theatre_area
(city, theatre_1, theatre_2, theatre_3, theatre_4)
VALUES
('CHENNAI', 'Cinemax Marina', 'Cinemax Velachery', 'Cinemax Anna Nagar', 'Cinemax OMR'),
('BENGALURU', 'Cinemax Koramangala', 'Cinemax Indiranagar', 'Cinemax Whitefield', 'Cinemax Yelahanka'),
('MUMBAI', 'Cinemax Andheri', 'Cinemax Bandra', 'Cinemax Powai', 'Cinemax Thane'),
('DELHI', 'Cinemax Saket', 'Cinemax Rohini', 'Cinemax Dwarka', 'Cinemax Rajouri'),
('KOLKATA', 'Cinemax Salt Lake', 'Cinemax Park Street', 'Cinemax New Town', 'Cinemax Behala')
ON DUPLICATE KEY UPDATE
    theatre_1 = VALUES(theatre_1),
    theatre_2 = VALUES(theatre_2),
    theatre_3 = VALUES(theatre_3),
    theatre_4 = VALUES(theatre_4);

INSERT INTO timeslot
(screen, slot_1, slot_2, slot_3, slot_4)
VALUES
('SCREEN-1', '10:00 AM', '01:30 PM', '05:00 PM', '08:30 PM'),
('SCREEN-2', '11:00 AM', '02:30 PM', '06:00 PM', '09:30 PM'),
('SCREEN-3', '09:30 AM', '12:45 PM', '04:15 PM', '07:45 PM')
ON DUPLICATE KEY UPDATE
    slot_1 = VALUES(slot_1),
    slot_2 = VALUES(slot_2),
    slot_3 = VALUES(slot_3),
    slot_4 = VALUES(slot_4);

INSERT INTO row_config (row_id, price)
VALUES
('A', 180), ('B', 180), ('C', 200),
('D', 200), ('E', 220), ('F', 220)
ON DUPLICATE KEY UPDATE price = VALUES(price);

INSERT INTO seat_config (seat_no)
VALUES
('1'), ('2'), ('3'), ('4'), ('5'),
('6'), ('7'), ('8'), ('9'), ('10')
ON DUPLICATE KEY UPDATE seat_no = VALUES(seat_no);

INSERT INTO foodbev_config (sno, snack_item, price)
VALUES
(1, 'Regular Popcorn', 180),
(2, 'Large Popcorn', 250),
(3, 'Nachos', 220),
(4, 'Soft Drink', 120),
(5, 'Combo Meal', 350),
(6, 'Mineral Water', 60)
ON DUPLICATE KEY UPDATE
    snack_item = VALUES(snack_item),
    price = VALUES(price);

-- Booking/payment tables are intentionally left empty.
-- app.py creates those records during an actual booking.
