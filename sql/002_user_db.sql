SET NAMES utf8mb4;

DROP TABLE IF EXISTS `USER`;
CREATE TABLE `USER` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each user',
  `NAME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Full name of the user',
  `USERNAME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Unique username for the user',
  `EMAIL` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Email address of the user',
  `PASSWORD_HASH` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Hashed password of the user',
  `BIRTH_DATE` date NOT NULL COMMENT 'Birth date of the user',
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