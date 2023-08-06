-- Adminer 4.8.1 MySQL 8.0.33 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `USER`;
CREATE TABLE `USER` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Table containing user information';


DROP TABLE IF EXISTS `DOCTOR_PATIENT_ASSOCIATION`;

-- Create the DOCTOR_PATIENT_ASSOCIATION table
CREATE TABLE `DOCTOR_PATIENT_ASSOCIATION` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each doctor-patient association',
  `DOCTOR_ID` int NOT NULL COMMENT 'ID of the doctor',
  `PATIENT_ID` int NOT NULL COMMENT 'ID of the patient',
  `STATUS` time NOT NULL COMMENT 'Status of the association',
  `CREATION_DATE` time NOT NULL COMMENT 'Date when the association was created',
  `LAST_UPDATE` timestamp NOT NULL COMMENT 'Date and time when the association was last updated',
  PRIMARY KEY (`ID`),
  KEY `DOCTOR_ID` (`DOCTOR_ID`),
  KEY `PATIENT_ID` (`PATIENT_ID`),
  CONSTRAINT `DOCTOR_PATIENT_ASSOCIATION_ibfk_1` FOREIGN KEY (`DOCTOR_ID`) REFERENCES `USER` (`ID`),
  CONSTRAINT `DOCTOR_PATIENT_ASSOCIATION_ibfk_2` FOREIGN KEY (`PATIENT_ID`) REFERENCES `USER` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Table containing doctor-patient association information';







