-- Run this block if you already have a database and need to re-create it
DELETE FROM Metals;
DELETE FROM Styles;
DELETE FROM Sizes;
DELETE FROM CUSTORDER;

DROP TABLE IF EXISTS CUSTORDER
DROP TABLE IF EXISTS Metals;
DROP TABLE IF EXISTS Styles;
DROP TABLE IF EXISTS Sizes;
-- End block

CREATE TABLE `Metals`(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Styles`(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(50) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Sizes`(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carats` NUMERIC(3) NOT NULL,
    `price` NUMERIC(6,2) NOT NULL
);

CREATE TABLE `CUSTORDER`(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal_id` INTEGER NOT NULL,
    FOREIGN KEY(`metal_id`) REFERENCES `Metals`(`id`),
    `carats_id` INTEGER NOT NULL,  
    FOREIGN KEY(`carats_id`) REFERENCES `Sizes`(`id`),
    `style_id` INTEGER NOT NULL,
    FOREIGN KEY(`style_id`) REFERENCES `Styles`(`id`),
    `price` NUMERIC NOT NULL
);

INSERT INTO `Metals` VALUES (null, 'Gold', 500.00)
INSERT INTO `Metals` VALUES (null, 'Silver', 450.00)

INSERT INTO `Sizes` VALUES (null, 24, 400.00)
INSERT INTO `Sizes` VALUES (null, 24, 400.00)

INSERT INTO `Styles` VALUES (null, 'Dainty', 200.00)
INSERT INTO `Styles` VALUES (null, 'Regal', 250.00)
