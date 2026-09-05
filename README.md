# CINEMAX — Movie Ticket Booking System

A web-based movie ticket booking application built with **Python Flask** and **MySQL**. The system provides an end-to-end booking workflow, from entering customer details and selecting a movie to choosing a show, reserving seats, ordering snacks, completing payment, and generating a downloadable ticket.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Application Workflow](#application-workflow)
- [Database](#database)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Movie Posters](#movie-posters)
- [Database Triggers](#database-triggers)
- [Important Implementation Notes](#important-implementation-notes)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

---

## Project Overview

**CINEMAX** is a cinema booking system designed to simulate the complete online movie-ticket reservation process.

The application uses Flask to handle HTTP requests, sessions, templates, and database operations. MySQL stores movie, theatre, show, seat, snack, booking, payment, and booking-log information.

The main booking flow is:

**Customer Details → Movies → Date → Theatre → Time Slot → Seats → Snacks → Payment → Invoice / Ticket**

---

## Features

### Customer Management
- Collects customer name, phone number, and city.
- Stores customer information temporarily using Flask sessions.
- Uses the customer's phone number to retrieve previous bookings.

### Movie Selection
- Displays currently available movies.
- Retrieves movie information from the MySQL `movies` table.
- Displays movie posters from the Flask `static/images` directory.
- Allows the customer to select a movie and screen.

### Date Selection
- Retrieves available dates associated with the selected movie.
- Presents the dates for customer selection.

### Theatre Selection
- Filters theatre options according to the customer's selected city.

### Show Time Selection
- Provides time slots associated with the selected screen.

### Seat Booking
- Displays configured seat rows and seat numbers.
- Shows already-booked seats.
- Allows customers to select multiple available seats.
- Calculates the ticket price according to the selected seat row.

### Food & Beverage Booking
- Displays available snacks and beverages.
- Allows customers to select quantities.
- Calculates the snack subtotal.

### Payment
- Calculates the combined seat and snack total.
- Records the selected payment method.
- Uses a database trigger to calculate the authoritative payment total.

### Invoice
- Displays:
  - Customer information
  - Movie
  - Selected seats
  - Snacks
  - Total amount

### Downloadable Ticket
- Generates a PDF ticket using ReportLab.
- Generates a QR code containing booking information.
- Allows the generated ticket to be downloaded.

### My Tickets
- Retrieves previous bookings using the customer's phone number.
- Displays booking ID, show information, number of seats, and total seat amount.

---

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python |
| Web Framework | Flask |
| Database | MySQL |
| Database Connector | MySQL connector used by `db.py` |
| Frontend | HTML5, CSS3, JavaScript |
| Templates | Jinja2 / Flask Templates |
| PDF Generation | ReportLab |
| QR Code | qrcode |
| Session Management | Flask Session |
| Styling | CSS + Google Fonts |

---

## Project Structure

A typical project structure is:

```text
CINEMAX/
│
├── app.py
├── db.py
│
├── sql/
│   ├── schema.sql
│   ├── seed.sql
│   ├── auto_update_total.sql
│   ├── block_duplicate_seats.sql
│   ├── log_bookings.sql
│
├── templates/
│   ├── index.html
│   ├── movies.html
│   ├── date.html
│   ├── theatre.html
│   ├── timeslot.html
│   ├── seats.html
│   ├── snacks.html
│   ├── payment.html
│   ├── invoice.html
│   └── tickets.html
│
└── static/
    └── images/
        ├── Antony.jpg
        ├── Atharva.jpg
        ├── Hi Nanna.jpg
        ├── Joram.jpg
        ├── 96.jpg
        ├── Operation Valentine.jpg
        ├── Philips.jpg
        ├── Silent Night.jpg
        ├── The Bikeriders.jpg
        └── Wonka.jpg
```

> **Important:** Flask looks for HTML templates in the `templates/` directory and static assets in the `static/` directory.

---

## Application Workflow

### 1. Customer Details

The application starts at `/`.

The customer enters:

- Name
- Phone number
- City

After submission, these values are stored in the Flask session and the customer is redirected to `/movies`.

### 2. Movie Selection

The `/movies` route queries the `movies` table and passes the results to `movies.html`.

The movie page uses the movie name to locate the corresponding poster:

```text
static/images/<movie_name>.jpg
```

For example:

```text
movie_name = "Hi Nanna"
```

requires:

```text
static/images/Hi Nanna.jpg
```

### 3. Date Selection

After a movie is selected, the application retrieves its `dates_available` value from the database and presents the available dates.

### 4. Theatre Selection

The selected city is used to retrieve the corresponding theatre options from `theatre_area`.

### 5. Time Slot Selection

The selected screen is used to retrieve its available slots from `timeslot`.

A `show_id` is then generated from:

```text
movie + date + timeslot
```

The selected show is stored in `movieshow_config`.

### 6. Seat Selection

The application checks `seat_booking` for seats already booked for the selected `show_id`.

The customer selects available seats.

The application determines each seat's price from `row_config` and creates the booking records.

### 7. Snacks

The customer can optionally select food and beverages.

The selected quantities are stored in `snack_booking`.

### 8. Payment

The payment page combines:

```text
Seat Total + Snack Total
```

The selected payment method is stored in `payment_details`.

### 9. Invoice

The invoice retrieves the seats and snacks belonging to the current `booking_id` and displays the booking summary.

### 10. Ticket PDF

The `/download_ticket` route generates:

- Booking information
- Seat information
- Snack information
- Total amount
- QR code

The ticket is returned as a downloadable PDF.

---

## Database

The application uses the following main tables:

| Table | Purpose |
|---|---|
| `movies` | Stores movie information and availability |
| `theatre_area` | Stores theatre options by city |
| `timeslot` | Stores show times for screens |
| `movieshow_config` | Stores selected show configurations |
| `row_config` | Defines seat rows and prices |
| `seat_config` | Defines seat numbers |
| `seat_booking` | Stores customer seat bookings |
| `foodbev_config` | Stores snacks and beverages |
| `snack_booking` | Stores selected snacks |
| `payment_details` | Stores payment information |
| `booking_log` | Stores booking log information |

---

## Setup and Installation

### Prerequisites

Install the following:

- Python 3
- MySQL Server
- MySQL Workbench or another MySQL client
- A modern web browser

### Python Dependencies

Install the required packages:

```bash
pip install flask mysql-connector-python reportlab qrcode[pil]
```

If the project contains a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

---

## Database Setup

### Step 1 — Create the Schema

Run:

```text
schema.sql
```

This creates the `movie_booking` database and its tables.

### Step 2 — Add Database Triggers

Run these SQL files after the schema:

```text
auto_update_total.sql
block_duplicate_seats.sql
log_bookings.sql
```

These provide:

- Automatic payment total calculation
- Duplicate-seat protection
- Booking logging

### Step 3 — Insert Demo Data

Run:

```text
seed.sql
```

The seed file inserts:

- Movies
- Theatre data
- Screen time slots
- Seat rows and prices
- Seat numbers
- Food and beverages

It intentionally does **not** insert real booking/payment records; those are created by the application during the booking process.

---

## Running the Application

### 1. Configure MySQL

Check `db.py` and make sure the database connection matches your MySQL installation.

Typical parameters include:

```text
host
user
password
database
```

The database should be:

```text
movie_booking
```

### 2. Start Flask

From the project directory:

```bash
python app.py
```

The Flask development server will start.

Open the local address shown in the terminal, normally:

```text
http://127.0.0.1:5000/
```

---

## Movie Posters

The movie listing page dynamically loads posters using the database movie name.

The relationship is:

```text
movies.movie_name
        ↓
movies.html
        ↓
static/images/<movie_name>.jpg
```

Therefore, the filenames must match the database movie names exactly.

### Current poster names

```text
Antony.jpg
Atharva.jpg
Hi Nanna.jpg
Joram.jpg
96.jpg
Operation Valentine.jpg
Philips.jpg
Silent Night.jpg
The Bikeriders.jpg
Wonka.jpg
```

If a poster is missing or incorrectly named, the movie card will not display the intended image.

---

## Database Triggers

The project contains three trigger scripts.

### `auto_update_total.sql`

Before a payment is inserted, the trigger calculates:

```text
Total = Seat Booking Amount + Snack Booking Amount
```

This prevents the stored payment total from depending solely on the value calculated by the frontend/application.

### `block_duplicate_seats.sql`

Prevents a seat from being booked twice for the same show.

This is important because seat availability can change between customers.

### `log_bookings.sql`

After a payment is inserted, the trigger creates an entry in `booking_log`.

This provides a basic booking history/audit mechanism.

---

## Important Implementation Notes

### `movies.html` is Required

`movies.html` is not database seed data.

It is the **presentation layer** for the movie-selection page.

`app.py` explicitly renders it:

```python
return render_template('movies.html', movies=movies)
```

Therefore, removing `movies.html` will cause the `/movies` route to fail.

### `seed.sql` and `movies.html` Have Different Jobs

| File | Responsibility |
|---|---|
| `seed.sql` | Inserts movie data into MySQL |
| `movies.html` | Displays movie data to the customer |
| `app.py` | Connects the webpage workflow to the database |
| Poster JPGs | Provide the visual movie images |

### Do Not Put Booking Data in `seed.sql`

The seed file is intended for initial/demo configuration.

Booking records should be generated by the application.

---

## Troubleshooting

### `TemplateNotFound: movies.html`

Make sure:

```text
templates/movies.html
```

exists.

### Posters Not Showing

Check that:

1. The `static/images` directory exists.
2. The poster is inside it.
3. The filename exactly matches the movie name in MySQL.
4. The `.jpg` extension is correct.

For example:

```text
Database:
Hi Nanna

File:
static/images/Hi Nanna.jpg
```

### MySQL Connection Error

Check:

- MySQL Server is running.
- Username is correct.
- Password is correct.
- Database name is `movie_booking`.
- `mysql-connector-python` is installed.

### No Movies Appearing

Verify that:

```sql
SELECT * FROM movies;
```

returns movie records.

If it returns no rows, run the corrected seed file.

### Duplicate Seat Error

This generally means another booking already contains the selected seat for the same show.

Refresh the seat-selection page and select only available seats.

---

## Future Enhancements

Possible improvements include:

- User authentication and account management
- Real payment gateway integration
- Email/SMS ticket delivery
- Real-time seat locking during checkout
- Admin dashboard
- Movie search and filtering
- Movie descriptions and trailers
- Theatre-specific screen configuration
- Better show-to-theatre relationships
- Booking cancellation and refunds
- QR-code ticket verification
- Responsive mobile UI
- Production-grade error handling
- Environment-variable based configuration
- Deployment using a production WSGI server

---

## Project Status

**Type:** Academic / Demonstration Project

**Backend:** Flask + MySQL

**Frontend:** HTML + CSS + JavaScript

**Core workflow:** Implemented

**Database:** Schema + seed data + triggers

**Ticket generation:** PDF + QR code

---

## License

This project is intended for educational and demonstration purposes. This was built for the Database Management Course Project.
