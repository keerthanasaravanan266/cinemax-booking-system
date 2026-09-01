DELIMITER $$

CREATE TRIGGER log_booking
AFTER INSERT ON payment_details
FOR EACH ROW
BEGIN
    INSERT INTO booking_log (booking_id)
    VALUES (NEW.booking_id);

END$$

DELIMITER ;

