-- Drop the MEDICAL_HISTORY table if it exists

DROP TABLE IF EXISTS `MEDICAL_HISTORY`;

-- Create the MEDICAL_HISTORY table

CREATE TABLE
    `MEDICAL_HISTORY` (
        `ID` INT NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each medical history record',
        `ASSOCIATION_ID` INT NOT NULL COMMENT 'ID of the doctor-patient association',
        `OBSERVATION` TEXT COMMENT 'Observations made during the visit',
        `DATE_OF_VISIT` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time of the visit',
        `NEXT_APPOINTMENT_DATE` DATETIME COMMENT 'Date and time of the next appointment',
        `DIAGNOSTIC` TEXT COMMENT 'diagnostic made during the visit',
        `PRESCRIPTION` TEXT COMMENT 'Prescription given during the visit',
        `SYMPTOMS` TEXT COMMENT 'Symptoms reported by the patient',
        `PRIVATE_NOTES` TEXT COMMENT 'Private notes about the visit',
        `FOLLOW_UP_REQUIRED` BOOLEAN DEFAULT FALSE COMMENT 'Whether a follow-up visit is required',
        `STATUS` BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Status of the medical history record',
        `CREATION_DATE` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time when the record was created',
        `LAST_UPDATE` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Date and time when the record was last updated',
        PRIMARY KEY (`ID`),
        FOREIGN KEY (`ASSOCIATION_ID`) REFERENCES `DOCTOR_PATIENT_ASSOCIATION`(`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Table containing medical history information';

-- Drop the MEDICAL_HISTORY_USER_IMAGE_ASSOCIATION table if it exists

DROP TABLE IF EXISTS `MEDICAL_HISTORY_USER_IMAGE_ASSOCIATION`;

-- Create the MEDICAL_HISTORY_USER_IMAGE_ASSOCIATION table

CREATE TABLE
    `MEDICAL_HISTORY_USER_IMAGE_ASSOCIATION` (
        `MEDICAL_HISTORY_ID` INT NOT NULL COMMENT 'ID of the medical history record',
        `USER_IMAGE_ID` INT NOT NULL COMMENT 'ID of the user image',
        PRIMARY KEY (
            `MEDICAL_HISTORY_ID`,
            `USER_IMAGE_ID`
        ),
        FOREIGN KEY (`MEDICAL_HISTORY_ID`) REFERENCES `MEDICAL_HISTORY`(`ID`),
        FOREIGN KEY (`USER_IMAGE_ID`) REFERENCES `USER_IMAGE`(`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Table containing associations between medical history records and user images';