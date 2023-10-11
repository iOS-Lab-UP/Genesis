DROP TABLE IF EXISTS `MEDICAL_HISTORY`;

CREATE TABLE
    `MEDICAL_HISTORY` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `association_id` INT NOT NULL,
        `observation` TEXT,
        `date_of_visit` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `next_appointment_date` DATETIME,
        `diagnosis` TEXT,
        `prescription` TEXT,
        `symptoms` TEXT,
        `private_notes` TEXT,
        `patient_feedback` TEXT,
        `follow_up_required` BOOLEAN DEFAULT FALSE,
        `status` BOOLEAN NOT NULL DEFAULT TRUE,
        `creation_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `last_update` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (`association_id`) REFERENCES `DOCTOR_PATIENT_ASSOCIATION`(`id`)
    );

DROP TABLE IF EXISTS `MEDICAL_HISTORY_USER_IMAGE_ASSOCIATION`;

CREATE TABLE
    `MEDICAL_HISTORY_USER_IMAGE_ASSOCIATION` (
        `medical_history_id` INT NOT NULL,
        `user_image_id` INT NOT NULL,
        PRIMARY KEY (
            `medical_history_id`,
            `user_image_id`
        ),
        FOREIGN KEY (`medical_history_id`) REFERENCES `MEDICAL_HISTORY`(`id`),
        FOREIGN KEY (`user_image_id`) REFERENCES `USER_IMAGE`(`id`)
    );