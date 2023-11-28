-- Adminer 4.8.1 MySQL 8.0.33 dump

SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `USER`;

CREATE TABLE
    `USER` (
        `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each user',
        `NAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Full name of the user',
        `USERNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Unique username for the user',
        `EMAIL` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Email address of the user',
        `PASSWORD_HASH` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Hashed password of the user',
        `BIRTH_DATE` date NOT NULL COMMENT 'Birth date of the user',
        `CEDULA` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'CEDULA of the user in case its a doctor',
        `PROFILE_ID` int NOT NULL COMMENT 'Foreign key from PROFILE table',
        `STATUS` tinyint NOT NULL DEFAULT '0' COMMENT 'Status of the user',
        `CREATION_DATE` date NOT NULL COMMENT 'Date when the user was created',
        `LAST_UPDATE` datetime NOT NULL COMMENT 'Date and time when the user was last updated',
        PRIMARY KEY (`ID`),
        KEY `IDX_USERNAME` (`USERNAME`),
        KEY `IDX_EMAIL` (`EMAIL`),
        KEY `IDX_CREATION_DATE` (`CREATION_DATE`),
        KEY `PROFILE_ID` (`PROFILE_ID`),
        CONSTRAINT `USER_ibfk_1` FOREIGN KEY (`PROFILE_ID`) REFERENCES `PROFILE` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Table containing user information';

DROP TABLE IF EXISTS `DOCTOR_PATIENT_ASSOCIATION`;

-- Create the DOCTOR_PATIENT_ASSOCIATION table

CREATE TABLE
    `DOCTOR_PATIENT_ASSOCIATION` (
        `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each doctor-patient association',
        `DOCTOR_ID` int NOT NULL COMMENT 'ID of the doctor',
        `PATIENT_ID` int NOT NULL COMMENT 'ID of the patient',
        `STATUS` tinyint NOT NULL DEFAULT '0' COMMENT 'Status of the Association',
        `CREATION_DATE` time NOT NULL COMMENT 'Date when the association was created',
        `LAST_UPDATE` timestamp NOT NULL COMMENT 'Date and time when the association was last updated',
        PRIMARY KEY (`ID`),
        KEY `DOCTOR_ID` (`DOCTOR_ID`),
        KEY `PATIENT_ID` (`PATIENT_ID`),
        CONSTRAINT `DOCTOR_PATIENT_ASSOCIATION_ibfk_1` FOREIGN KEY (`DOCTOR_ID`) REFERENCES `USER` (`ID`),
        CONSTRAINT `DOCTOR_PATIENT_ASSOCIATION_ibfk_2` FOREIGN KEY (`PATIENT_ID`) REFERENCES `USER` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'Table containing doctor-patient association information';

INSERT INTO
    `USER` (
        `ID`,
        `NAME`,
        `USERNAME`,
        `EMAIL`,
        `PASSWORD_HASH`,
        `BIRTH_DATE`,
        `CEDULA`,
        `PROFILE_ID`,
        `STATUS`,
        `CREATION_DATE`,
        `LAST_UPDATE`
    )
VALUES (
        1,
        'Luis Cedillo Maldonado',
        'luisced',
        'luisitocedillo@gmail.com',
        '$2b$12$cHA.Gji6IG1iKTqh32pZbOMn4dRGfoMEK5p7lIsr0JvEaTUPS5MaW',
        '2003-02-01',
        NULL,
        1,
        1,
        '2023-11-07',
        '2023-11-07 13:40:55'
    ), (
        2,
        'Jane Smith',
        'jane_smith',
        'jane.smith@example.com',
        'hashed_password2',
        '1985-08-25',
        NULL,
        2,
        0,
        '2023-01-11',
        '2023-11-07 10:15:00'
    ), (
        3,
        'Mónica Fuentes Ruiz',
        'monica_fuentes',
        'dr.smith@example.com',
        '$2b$12$cHA.Gji6IG1iKTqh32pZbOMn4dRGfoMEK5p7lIsr0JvEaTUPS5MaW',
        '1975-03-12',
        '12345',
        3,
        1,
        '2023-01-12',
        '2023-11-07 11:45:00'
    ), (
        4,
        'Dr. Johnson',
        'dr_johnson',
        'dr.johnson@example.com',
        'hashed_password4',
        '1980-11-28',
        '54321',
        3,
        0,
        '2023-01-13',
        '2023-11-07 12:30:00'
    ), (
        5,
        'Mary Brown',
        'mary_brown',
        'mary.brown@example.com',
        'hashed_password5',
        '1995-09-20',
        NULL,
        4,
        1,
        '2023-01-14',
        '2023-11-07 13:20:00'
    );

-- Dummy data for the DOCTOR_PATIENT_ASSOCIATION table

INSERT INTO
    `DOCTOR_PATIENT_ASSOCIATION` (
        `DOCTOR_ID`,
        `PATIENT_ID`,
        `STATUS`,
        `CREATION_DATE`,
        `LAST_UPDATE`
    )
VALUES (
        3,
        1,
        1,
        '2023-01-15',
        '2023-11-07 14:10:00'
    ), (
        3,
        2,
        1,
        '2023-01-16',
        '2023-11-07 15:00:00'
    ), (
        4,
        2,
        0,
        '2023-01-17',
        '2023-11-07 16:30:00'
    ), (
        5,
        3,
        0,
        '2023-01-18',
        '2023-11-07 17:15:00'
    );