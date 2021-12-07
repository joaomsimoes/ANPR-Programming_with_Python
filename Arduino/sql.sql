###########################
##### Procedure List #####
###########################

CREATE PROCEDURE empty_parking_place(
    IN s_plate varchar(45)
    )
BEGIN
    UPDATE free_places SET free = 0, plate = null
    WHERE plate = s_plate;
END $$

############################

CREATE PROCEDURE entry_time(
    IN s_plate varchar(45)
    )
BEGIN
    SELECT entry_time
    FROM entries
    WHERE plate = s_plate
    ORDER BY id
    DESC LIMIT 1;
END $$

############################

CREATE PROCEDURE free_place()
BEGIN
    SELECT id
    FROM free_places
    WHERE free = 0;
END $$

############################

CREATE PROCEDURE ocupy_place(
    IN s_plate varchar(45),
    IN s_place int
)
BEGIN
    UPDATE free_places SET free = 1, plate = s_plate
    WHERE id = s_place;
END $$

############################

CREATE PROCEDURE payment(
    IN s_plate varchar(45),
    IN s_total_time int,
    IN s_total_cost float
)
BEGIN
    INSERT INTO payments (plate, total_time, cost)
    VALUES (s_plate, s_total_time, s_total_cost);
END $$

############################

CREATE PROCEDURE entry(
    IN s_plate varchar(45),
    IN s_entry_time datetime
)
BEGIN
    INSERT INTO entries (plate, entry_time)
    VALUES (s_plate, s_entry_time);
END $$

############################

CREATE PROCEDURE exit_park(
    IN s_plate varchar(45),
    IN s_exit_time datetime
)
BEGIN
    INSERT INTO entries (plate, exit_time)
    VALUES (s_plate, s_exit_time);
END $$

############################

CREATE PROCEDURE verify_car_is_parked(
    IN s_plate varchar(45)
)
BEGIN
    SELECT IF(plate IS NULL, 0, 1)
    FROM free_places WHERE plate = s_plate;
END $$

############################