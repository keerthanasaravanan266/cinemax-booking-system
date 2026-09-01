DELIMITER $$

CREATE TRIGGER prevent_double_booking
BEFORE INSERT ON seat_booking
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM seat_booking
        WHERE show_id = NEW.show_id
        AND row_id = NEW.row_id
        AND seat_no = NEW.seat_no
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Seat already booked!';
    END IF;
END$$

DELIMITER ;