-- Drop the MEDICAL_HISTORY table if it exists

DROP TABLE IF EXISTS `PRESCRIPTION`;
CREATE TABLE `PRESCRIPTION` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each prescription',
  `TREATMENT` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Name of the medicine prescribed',
  `INDICATIONS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT 'Detailed indications for the patient',
  `DOSAGE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Dosage of the medicine',
  `FREQUENCY_VALUE` int NOT NULL COMMENT 'The numerical value of the frequency (e.g., every 2 hours, every 3 days, etc.)',
  `FREQUENCY_UNIT` enum('minute','hour','day','week','month') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'The unit of time for the frequency (minutes, hours, days, weeks, or months)',
  `START_DATE` datetime NOT NULL COMMENT 'Start date of the medication',
  `END_DATE` datetime DEFAULT NULL COMMENT 'End date of the medication, can be NULL if indefinite or as needed',
  `NOTIFICATIONS_ENABLED` tinyint(1) DEFAULT '1' COMMENT 'Whether notifications for this prescription are enabled',
  `CREATION_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time when the prescription was created',
  `LAST_UPDATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Date and time when the prescription was last updated',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Table containing prescription information';




DROP TABLE IF EXISTS `MEDICAL_HISTORY`;

-- Create the MEDICAL_HISTORY table
DROP TABLE IF EXISTS `MEDICAL_HISTORY`;
CREATE TABLE `MEDICAL_HISTORY` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each medical history record',
  `ASSOCIATION_ID` int NOT NULL COMMENT 'ID of the doctor-patient association',
  `OBSERVATION` text COLLATE utf8mb4_unicode_ci COMMENT 'Observations made during the visit',
  `DATE_OF_VISIT` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time of the visit',
  `NEXT_APPOINTMENT_DATE` datetime DEFAULT NULL COMMENT 'Date and time of the next appointment',
  `DIAGNOSTIC` text COLLATE utf8mb4_unicode_ci COMMENT 'diagnostic made during the visit',
  `PRESCRIPTION_ID` int DEFAULT NULL COMMENT 'Prescription given during the visit',
  `SYMPTOMS` text COLLATE utf8mb4_unicode_ci COMMENT 'Symptoms reported by the patient',
  `PRIVATE_NOTES` text COLLATE utf8mb4_unicode_ci COMMENT 'Private notes about the visit',
  `FOLLOW_UP_REQUIRED` tinyint(1) DEFAULT '0' COMMENT 'Whether a follow-up visit is required',
  `STATUS` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'Status of the medical history record',
  `CREATION_DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time when the record was created',
  `LAST_UPDATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Date and time when the record was last updated',
  PRIMARY KEY (`ID`),
  KEY `ASSOCIATION_ID` (`ASSOCIATION_ID`),
  KEY `PRESCRIPTION_ID` (`PRESCRIPTION_ID`),
  CONSTRAINT `MEDICAL_HISTORY_ibfk_1` FOREIGN KEY (`ASSOCIATION_ID`) REFERENCES `DOCTOR_PATIENT_ASSOCIATION` (`ID`),
  CONSTRAINT `MEDICAL_HISTORY_ibfk_2` FOREIGN KEY (`PRESCRIPTION_ID`) REFERENCES `PRESCRIPTION` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Table containing medical history information';

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