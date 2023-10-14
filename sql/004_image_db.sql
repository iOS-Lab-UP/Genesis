SET NAMES utf8mb4;

-- Drop the table if it exists

DROP TABLE IF EXISTS `IMAGE`;

-- Create the IMAGE table

CREATE TABLE
    `IMAGE` (
        `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each image',
        `PATH` varchar(255) NOT NULL COMMENT 'Path to the image file',
        `NAME` varchar(255) NOT NULL COMMENT 'Name of the image',
        `CREATION_DATE` date NOT NULL COMMENT 'Date when the image was created',
        `LAST_UPDATE` timestamp NOT NULL COMMENT 'Date and time when the image was last updated',
        `STATUS` tinyint NOT NULL COMMENT 'Status of the image',
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'Table containing image information';

-- Drop the table if it exists

DROP TABLE IF EXISTS `USER_IMAGE`;

-- Create the USER_IMAGE table

CREATE TABLE
    `USER_IMAGE` (
        `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each user image',
        `USER_ID` int NOT NULL COMMENT 'ID of the user who uploaded the image',
        `IMAGE_ID` int NOT NULL COMMENT 'ID of the image',
        `STATUS` tinyint NOT NULL COMMENT 'Status of the image',
        `CREATION_DATE` date NOT NULL COMMENT 'Date when the image was created',
        `LAST_UPDATE` timestamp NOT NULL COMMENT 'Date and time when the image was last updated',
        PRIMARY KEY (`ID`),
        KEY `USER_ID` (`USER_ID`),
        KEY `IMAGE_ID` (`IMAGE_ID`),
        CONSTRAINT `USER_IMAGE_ibfk_1` FOREIGN KEY (`USER_ID`) REFERENCES `USER` (`ID`),
        CONSTRAINT `USER_IMAGE_ibfk_2` FOREIGN KEY (`IMAGE_ID`) REFERENCES `IMAGE` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'Table containing user image information';