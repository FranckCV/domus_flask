

DELIMITER //
CREATE TRIGGER reducir_stock
AFTER UPDATE ON pedido
FOR EACH ROW
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE cantidad INT;
    DECLARE productoid INT;

    DECLARE cursor_cantidad CURSOR FOR 
        SELECT dp.cantidad, dp.productoid 
        FROM detalles_pedido dp 
        WHERE dp.pedidoid = NEW.id;

    -- Si ya no encuentra más filas para recorrer, termina el cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cursor_cantidad;

    read_loop: LOOP
        FETCH cursor_cantidad INTO cantidad, productoid;

        IF done THEN
            LEAVE read_loop;
        END IF;

        UPDATE producto
        SET stock = stock - cantidad
        WHERE id = productoid;

    END LOOP;

    CLOSE cursor_cantidad;
END;
//
DELIMITER ;





DELIMITER //

CREATE TRIGGER check_stock_before_insert
BEFORE INSERT ON detalles_pedido
FOR EACH ROW
BEGIN
    DECLARE stock_disponible INT;

    SELECT stock INTO stock_disponible FROM producto WHERE id = NEW.productoid;

    IF New.cantidad > stock_disponible THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'La cantidad solicitada excede el stock disponible';
    END IF;
END;
//

DELIMITER ;


DELIMITER //

CREATE TRIGGER check_stock_before_update
BEFORE UPDATE ON detalles_pedido
FOR EACH ROW
BEGIN
    DECLARE stock_disponible INT;
    DECLARE cantidad_en_carrito INT DEFAULT 0;
    DECLARE mensaje_error VARCHAR(255);

    SELECT stock INTO stock_disponible FROM producto WHERE id = NEW.productoid;

    IF NEW.cantidad > stock_disponible THEN
        SET mensaje_error = CONCAT('La cantidad solicitada (', NEW.cantidad, 
                                   ') excede el stock disponible. Stock disponible: ', 
                                   stock_disponible);  
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mensaje_error;
    END IF;
END;
//

DELIMITER ;





