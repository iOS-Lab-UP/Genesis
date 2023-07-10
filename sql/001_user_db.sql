SET NAMES utf8mb4;

CREATE TABLE `USER` (
    `ID` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each user',
    `NAME` VARCHAR(255) NOT NULL COMMENT 'Full name of the user',
    `USERNAME` VARCHAR(255) NOT NULL COMMENT 'Unique username for the user',
    `EMAIL` VARCHAR(255) NOT NULL COMMENT 'Email address of the user',
    `PASSWORD_HASH` VARCHAR(255) NOT NULL COMMENT 'Hashed password of the user',
    `BIRTH_DATE` DATE COMMENT 'Birth date of the user',
    `STATUS` TINYINT(4) NOT NULL DEFAULT '0' COMMENT 'Status of the user',
    `CREATION_DATE` DATE NOT NULL COMMENT 'Date when the user was created',
    `LAST_UPDATE` DATETIME NOT NULL COMMENT 'Date and time when the user was last updated',
    PRIMARY KEY (`ID`),
    INDEX `IDX_USERNAME` (`USERNAME`),
    INDEX `IDX_EMAIL` (`EMAIL`),
    INDEX `IDX_CREATION_DATE` (`CREATION_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Table containing user information';