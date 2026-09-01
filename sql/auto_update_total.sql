DELIMITER $$

CREATE TRIGGER update_payment_total
BEFORE INSERT ON payment_details
FOR EACH ROW
BEGIN
    DECLARE seat_sum INT;
    DECLARE snack_sum INT;

    SELECT IFNULL(SUM(price),0) INTO seat_sum
    FROM seat_booking
    WHERE booking_id = NEW.booking_id;

    SELECT IFNULL(SUM(amount),0) INTO snack_sum
    FROM snack_booking
    WHERE booking_id = NEW.booking_id;

    SET NEW.total_amount = seat_sum + snack_sum;
END$$
DELIMITER ;