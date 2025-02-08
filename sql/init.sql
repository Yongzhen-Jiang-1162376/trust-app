CREATE TABLE `auth_user` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`email` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`password` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`full_name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`is_active` TINYINT(1) NOT NULL DEFAULT '1',
	`is_blocked` TINYINT(1) NOT NULL DEFAULT '0',
	`is_superadmin` TINYINT(1) NOT NULL DEFAULT '0',
	`title` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`created_at` DATETIME NULL DEFAULT NULL,
	`created_by_id` INT NULL DEFAULT NULL,
	`updated_at` DATETIME NULL DEFAULT NULL,
	`updated_by_id` INT NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `email` (`email`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

CREATE TABLE `hr_employee` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`full_name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`gender` VARCHAR(6) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`position` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`manager_name` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`employee_type` VARCHAR(9) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`mode_of_work` VARCHAR(6) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`date_of_birth` DATE NULL DEFAULT NULL,
	`nationality` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`email` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`contact_detail` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`address` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`start_date` DATE NULL DEFAULT NULL,
	`resignation_date` DATE NULL DEFAULT NULL,
	`leave_reason` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`last_working_date` DATE NULL DEFAULT NULL,
	`trial_period` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`trial_period_start_date` DATE NULL DEFAULT NULL,
	`hours_per_week` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`volunteer_current_status` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`feedback_performance_review` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`comments` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`created_at` DATETIME NULL DEFAULT NULL,
	`created_by_id` INT NULL DEFAULT NULL,
	`updated_at` DATETIME NULL DEFAULT NULL,
	`updated_by_id` INT NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;

CREATE TABLE `hr_employee_document` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`employee_id` INT NOT NULL,
	`original_file_name` TEXT NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`extension` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`file_uuid` VARCHAR(36) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`file_name` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`created_at` DATETIME NULL DEFAULT NULL,
	`created_by_id` INT NULL DEFAULT NULL,
	`updated_at` DATETIME NULL DEFAULT NULL,
	`updated_by_id` INT NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `employee_id` (`employee_id`) USING BTREE,
	CONSTRAINT `hr_employee_document_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `hr_employee` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


CREATE TABLE `hr_employee_portfolio_group` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`group_name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


CREATE TABLE `hr_employee_portfolio` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`group_id` INT NOT NULL,
	`portfolio` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `group_id` (`group_id`) USING BTREE,
	CONSTRAINT `hr_employee_portfolio_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `hr_employee_portfolio_group` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


CREATE TABLE `hr_employee_portfolio_assigned` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`employee_id` INT NOT NULL,
	`portfolio_id` INT NOT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `employee_id` (`employee_id`) USING BTREE,
	INDEX `portfolio_id` (`portfolio_id`) USING BTREE,
	CONSTRAINT `hr_employee_portfolio_assigned_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `hr_employee` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `hr_employee_portfolio_assigned_ibfk_2` FOREIGN KEY (`portfolio_id`) REFERENCES `hr_employee_portfolio` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1
;


CREATE TABLE `auth_user_portfolio` (
	`user_id` INT NOT NULL,
	`portfolio_id` INT NOT NULL,
	PRIMARY KEY (`user_id`, `portfolio_id`) USING BTREE,
	INDEX `portfolio_id` (`portfolio_id`) USING BTREE,
	CONSTRAINT `auth_user_portfolio_ibfk_1` FOREIGN KEY (`portfolio_id`) REFERENCES `hr_employee_portfolio` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `auth_user_portfolio_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;



INSERT INTO hr_employee_portfolio_group (GROUP_name)
VALUES
('Trust Governance_Taumata Advisor Portfolio'), 
('Trust Corporate Portfolio'), 
('Trust Operations Management Portfolio')
;


INSERT INTO hr_employee_portfolio (group_id, portfolio)
VALUES 	 (1, 'Health Advisors - Mental'),
		 (1, 'Health Advisors - Disability'),
		 (1, 'Health Advisors - General'),
		 (1, 'Environment Advisors - Water Care'),
		 (1, 'Environment Advisors - Climate Change'),
		 (1, 'Environment Advisors - Food Sovereignty'),
		 (1, 'Education Advisors - Kura Kaupapa (Maori Language Schools)'),
		 (1, 'Education Advisors - Kura Kaupapa (General Schools)'),
		 (1, 'Cultural Advisors'),
		 (1, 'Whenua (Land) Advisors - Maori Land'),
		 (1, 'Whenua (Land) Advisors - General Land'),
		 (1, 'Policy Planner Advisors'),
		 (1, 'Political Advisors'),
		 (2, 'Trust Corporate Team (Chairperson / CEO)'),
		 (2, 'PA Corporate Management Portfolio'),
		 (2, 'Finance Operations'),
		 (2, 'Legal Team'),
		 (2, 'Chartered Accountant'),
		 (3, 'Business Development Management Portfolio'),
		 (3, 'Office and Human Resource Management Team'),
		 (3, 'Business Analysis Management Portfolio'),
		 (3, 'Policy Analyst Researcher Management Portfolio'),
		 (3, 'Project Management Portfolio'),
		 (3, 'Website Management Portfolio'),
		 (3, 'Software Development Management Portfolio'),
		 (3, 'Information Technology Management Portfolio'),
		 (3, 'Business Development Management Portfolio'),
		 (3, 'Graphic Design Management Portfolio'),
		 (3, 'Marketing Management Portfolio'),
		 (3, 'Events-Coordinator Management Portfolio'),
		 (3, 'Funding Mobilization Management Portfolio'),
		 (3, 'Artificial Intelligence Management Portfolio'),
		 (3, 'Cyber Security Management Portfolio')
;
