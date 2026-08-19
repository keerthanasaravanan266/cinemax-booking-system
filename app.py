from flask import Flask, render_template, request, redirect, session
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import qrcode
from db import get_db
import uuid

import os
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "development-secret-key")


# HOME
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['phone'] = request.form['phone']
        session['city'] = request.form['city']
        return redirect('/movies')
    return render_template('index.html')


# MOVIES
@app.route('/movies')
def movies():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return render_template('movies.html', movies=movies)


# SELECT MOVIE
@app.route('/select_movie', methods=['POST'])
def select_movie():
    session['movie'] = request.form['movie']
    session['screen'] = request.form['screen']
    return redirect('/select_date')

@app.route('/select_date')
def select_date():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT dates_available FROM movies WHERE movie_name=%s", (session['movie'],))
    result = cursor.fetchone()

    dates = result[0].split(',')

    return render_template('date.html', dates=dates)


@app.route('/save_date', methods=['POST'])
def save_date():
    session['date'] = request.form['date']
    return redirect('/theatre')

# THEATRE
@app.route('/theatre')
def theatre():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM theatre_area WHERE city=%s", (session['city'],))
    data = cursor.fetchall()

    return render_template('theatre.html', data=data)


@app.route('/select_theatre', methods=['POST'])
def select_theatre():
    session['theatre_id'] = request.form['theatre']
    return redirect('/timeslot')


# TIMESLOT
@app.route('/timeslot')
def timeslot():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM timeslot WHERE screen=%s", (session['screen'],))
    data = cursor.fetchall()

    return render_template('timeslot.html', data=data)


@app.route('/select_timeslot', methods=['POST'])
def select_timeslot():
    session['timeslot'] = request.form['timeslot']

    show_id = f"{session['movie']}_{session['date']}_{session['timeslot']}"
    session['show_id'] = show_id

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO movieshow_config 
        (movie_name, theatre_code, screencode, show_id, show_date, timeslot)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        session['movie'],
        session['theatre_id'],
        session['screen'],
        show_id,
        session['date'],
        session['timeslot']
    ))

    db.commit()
    return redirect('/seats')


# SEATS
@app.route('/seats')
def seats():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT row_id, seat_no 
        FROM seat_booking 
        WHERE show_id=%s
    """, (session['show_id'],))
    booked = cursor.fetchall()

    cursor.execute("SELECT * FROM row_config")
    rows = cursor.fetchall()

    cursor.execute("SELECT * FROM seat_config")
    seats = cursor.fetchall()

    return render_template('seats.html', rows=rows, seats=seats, booked=booked)


# BOOK SEATS
@app.route('/book_seats', methods=['POST'])
def book_seats():
    selected = request.form['selected_seats'].split(',')

    db = get_db()
    cursor = db.cursor()

    booking_id = str(uuid.uuid4())[:8]
    session['booking_id'] = booking_id

    total = 0

    for seat in selected:
        if seat:
            row, seat_no = seat.split('-')

            cursor.execute("SELECT price FROM row_config WHERE row_id=%s", (row,))
            price = cursor.fetchone()[0]

            total += price

            cursor.execute("""
                INSERT INTO seat_booking 
                (phno, show_id, row_id, seat_no, price, booking_date, booking_id)
                VALUES (%s, %s, %s, %s, %s, NOW(), %s)
            """, (
                session['phone'],
                session['show_id'],
                row,
                seat_no,
                price,
                booking_id
            ))

    db.commit()
    session['seat_total'] = total

    return redirect('/snacks')


# SNACKS
@app.route('/snacks')
def snacks():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM foodbev_config")
    snacks = cursor.fetchall()

    return render_template('snacks.html', snacks=snacks)


@app.route('/add_snacks', methods=['POST'])
def add_snacks():
    db = get_db()
    cursor = db.cursor()

    total = 0

    for key in request.form:
        qty = int(request.form[key])

        if qty > 0:
            cursor.execute("SELECT * FROM foodbev_config WHERE sno=%s", (key,))
            item = cursor.fetchone()

            amount = item[2] * qty
            total += amount

            cursor.execute("""
                INSERT INTO snack_booking 
                (phno, show_id, snack_no, snack_item, quantity, amount, booking_time, booking_id)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
            """, (
                session['phone'],
                session['show_id'],
                key,
                item[1],
                qty,
                amount,
                session['booking_id']
            ))

    db.commit()
    session['snack_total'] = total

    return redirect('/payment')


# PAYMENT
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    total = session.get('seat_total', 0) + session.get('snack_total', 0)

    if request.method == 'POST':
        method = request.form['method']

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO payment_details 
            (phno, show_id, payment_method, total_amount, booking_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            session['phone'],
            session['show_id'],
            method,
            total,
            session['booking_id']
        ))

        db.commit()

        return redirect('/invoice')

    return render_template('payment.html', total=total)


# INVOICE
@app.route('/invoice')
def invoice():
    db = get_db()
    cursor = db.cursor()

    booking_id = session['booking_id']

    cursor.execute("""
        SELECT row_id, seat_no, price 
        FROM seat_booking 
        WHERE booking_id=%s
    """, (booking_id,))
    seats = cursor.fetchall()

    cursor.execute("""
        SELECT snack_item, quantity, amount 
        FROM snack_booking 
        WHERE booking_id=%s
    """, (booking_id,))
    snacks = cursor.fetchall()

    total = session.get('seat_total', 0) + session.get('snack_total', 0)

    return render_template('invoice.html', seats=seats, snacks=snacks, total=total)

@app.route('/download_ticket')
def download_ticket():
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    import qrcode

    db = get_db()
    cursor = db.cursor()

    booking_id = session['booking_id']

    cursor.execute("""
        SELECT row_id, seat_no, price 
        FROM seat_booking WHERE booking_id=%s
    """, (booking_id,))
    seats = cursor.fetchall()

    cursor.execute("""
        SELECT snack_item, quantity, amount 
        FROM snack_booking WHERE booking_id=%s
    """, (booking_id,))
    snacks = cursor.fetchall()

    total = session.get('seat_total', 0) + session.get('snack_total', 0)

    # QR
    qr_data = f"Booking:{booking_id}|Movie:{session['movie']}|Phone:{session['phone']}"
    qr = qrcode.make(qr_data)
    qr_path = "qr.png"
    qr.save(qr_path)

    # PDF
    file_path = "ticket.pdf"
    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    # CUSTOM STYLES
    title_style = ParagraphStyle(
        'title',
        fontSize=20,
        textColor=colors.white,
        alignment=1,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        'normal',
        fontSize=11,
        spaceAfter=5
    )

    section_style = ParagraphStyle(
        'section',
        fontSize=14,
        textColor=colors.red,
        spaceAfter=8
    )

    elements = []

    # HEADER BAR
    header = Table([[" MOVIE TICKET"]], colWidths=[450])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.red),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTSIZE',(0,0),(-1,-1),18),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12)
    ]))
    elements.append(header)
    elements.append(Spacer(1, 15))

    # INFO CARD
    info_data = [
        ["Booking ID:", booking_id],
        ["Name:", session['name']],
        ["Phone:", session['phone']],
        ["Movie:", session['movie']]
    ]

    info_table = Table(info_data, colWidths=[120, 300])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
        ('BOX', (0,0), (-1,-1), 1, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # SEATS
    elements.append(Paragraph(" Seats", section_style))

    seat_data = [["Row", "Seat", "Price"]]
    for s in seats:
        seat_data.append([s[0], s[1], f"Rs. {s[2]}"])

    seat_table = Table(seat_data, colWidths=[80, 80, 100])
    seat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.red),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))

    elements.append(seat_table)
    elements.append(Spacer(1, 20))

    # SNACKS
    elements.append(Paragraph(" Snacks", section_style))

    if snacks:
        snack_data = [["Item", "Qty", "Amount"]]
        for s in snacks:
            snack_data.append([s[0], s[1], f"Rs. {s[2]}"])

        snack_table = Table(snack_data, colWidths=[150, 80, 100])
        snack_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))

        elements.append(snack_table)
    else:
        elements.append(Paragraph("No snacks ordered", normal_style))

    elements.append(Spacer(1, 20))

    # TOTAL BOX
    total_box = Table([[f"TOTAL PAID: Rs. {total}"]], colWidths=[250])
    total_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.black),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTSIZE',(0,0),(-1,-1),14),
        ('PADDING', (0,0), (-1,-1), 10)
    ]))

    elements.append(total_box)
    elements.append(Spacer(1, 25))

    # QR + TEXT 
    qr_img = Image(qr_path, width=120, height=120)

    qr_table = Table([
        ["Scan for entry", qr_img]
    ], colWidths=[200, 150])

    qr_table.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ALIGN',(1,0),(1,0),'CENTER')
    ]))

    elements.append(qr_table)

    doc.build(elements)

    from flask import send_file
    return send_file(file_path, as_attachment=True)

# MY TICKETS
@app.route('/my_tickets')
def my_tickets():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT booking_id, show_id, COUNT(*), SUM(price)
        FROM seat_booking
        WHERE phno=%s
        GROUP BY booking_id, show_id
    """, (session['phone'],))

    tickets = cursor.fetchall()

    return render_template('tickets.html', tickets=tickets)


# RUN
if __name__ == '__main__':
    app.run(debug=True)