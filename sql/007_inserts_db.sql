SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

INSERT INTO
    `IMAGE` (
        `ID`,
        `PATH`,
        `NAME`,
        `CREATION_DATE`,
        `LAST_UPDATE`,
        `STATUS`
    )
VALUES (
        1,
        'App/genesis_api/static/uploads/IMG-20211104-WA0016_Original.jpg',
        'IMG-20211104-WA0016_Original.jpg',
        '2023-11-22',
        '2023-11-22 21:39:14',
        1
    );

INSERT INTO
    `ML_DIAGNOSTIC` (
        `ID`,
        `SICKNESS`,
        `DESCRIPTION`,
        `PRECISION`,
        `STATUS`,
        `CREATION_DATE`,
        `LAST_UPDATE`
    )
VALUES (
        1,
        'Carcinoma',
        'Null',
        0.8,
        1,
        '2023-11-22',
        '2023-11-22 21:40:11'
    ), (
        2,
        'Melanoma',
        'Null',
        0.1,
        1,
        '2023-11-22',
        '2023-11-22 21:40:26'
    ), (
        3,
        'Monkey-Pox',
        'Null',
        0.1,
        1,
        '2023-11-22',
        '2023-11-22 21:40:45'
    );

INSERT INTO
    `USER_IMAGE` (
        `ID`,
        `USER_ID`,
        `IMAGE_ID`,
        `STATUS`,
        `CREATION_DATE`,
        `LAST_UPDATE`
    )
VALUES (
        1,
        1,
        1,
        1,
        '2023-11-22',
        '2023-11-22 21:39:29'
    );

INSERT INTO
    `PRESCRIPTION` (
        `ID`,
        `TREATMENT`,
        `INDICATIONS`,
        `DOSAGE`,
        `FREQUENCY_VALUE`,
        `FREQUENCY_UNIT`,
        `START_DATE`,
        `END_DATE`,
        `NOTIFICATIONS_ENABLED`,
        `STATUS`,
        `CREATION_DATE`,
        `LAST_UPDATE`
    )
VALUES (
        1,
        'Ibuprofen',
        'Comprar en Simi',
        '256 mgs',
        2,
        'hour',
        '2023-11-22 21:45:39',
        '2023-12-30 00:00:00',
        1,
        1,
        '2023-11-22 21:45:39',
        '2023-11-22 21:45:39'
    );

INSERT INTO
    `MEDICAL_HISTORY` (
        `ID`,
        `ASSOCIATION_ID`,
        `OBSERVATION`,
        `DATE_OF_VISIT`,
        `NEXT_APPOINTMENT_DATE`,
        `DIAGNOSTIC`,
        `SYMPTOMS`,
        `PRIVATE_NOTES`,
        `FOLLOW_UP_REQUIRED`,
        `PATIENT_FEEDBACK`,
        `STATUS`,
        `CREATION_DATE`,
        `LAST_UPDATE`
    )
VALUES (
        1,
        1,
        'Está malito',
        '2023-11-22 21:44:44',
        '2023-11-30 00:00:00',
        'Cáncer',
        'Comezón',
        'Se va a morir',
        1,
        '',
        1,
        '2023-11-22 21:44:44',
        '2023-11-22 21:44:44'
    );

INSERT INTO
    `MEDICAL_HISTORY_PRESCRIPTION_ASSOCIATION` (
        `ID`,
        `MEDICAL_HISTORY_ID`,
        `PRESCRIPTION_ID`
    )
VALUES (1, 1, 1);

INSERT INTO
    `MEDICAL_HISTORY_USER_IMAGE_ASSOCIATION` (
        `MEDICAL_HISTORY_ID`,
        `USER_IMAGE_ID`
    )
VALUES (1, 1);

INSERT INTO
    `USER_IMAGE_ML_DIAGNOSTIC_ASSOCIATION` (
        `ID`,
        `USER_IMAGE`,
        `ML_DIAGNOSTIC`
    )
VALUES (1, 1, 1), (2, 1, 2), (3, 1, 3);