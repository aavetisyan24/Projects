
CREATE TABLE Consumers (
    Platform varchar(255),
    ScreenAUsers Int,
    Subscribed Int
);

INSERT INTO Consumers VALUES ("Android", 120000, 940);
INSERT INTO Consumers VALUES ("IOS", 32000, 460);

SELECT Platform, MAX(ROUND(Subscribed * 100.0 / ScreenAUsers, 1)) AS Percent FROM Consumers;


select * from Consumers;





CREATE TABLE Actions (
    Date date,
    DeviceID varchar(255),
    ProductID Int,
    EventName varchar(255)
);

INSERT INTO Actions VALUES ("2019-03-01", "a1b1c1", 123, "photo_open");
INSERT INTO Actions VALUES ("2019-03-01", "a1b1c1", 123, "photo_like");
INSERT INTO Actions VALUES ("2019-03-02", "a1b2c0", 124, "photo_open");
INSERT INTO Actions VALUES ("2019-03-02", "a1b3cd", 234, "photo_open");
INSERT INTO Actions VALUES ("2019-03-04", "a1b4ce", 123, "photo_open");

SELECT Date, DeviceID, ProductID, EventName FROM Actions WHERE EventName='photo_open' OR EventName='photo_like';


select * from Actions;
