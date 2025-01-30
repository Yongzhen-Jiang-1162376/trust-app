-- SELECT * FROM hr_employee_portfolio;
-- SELECT * FROM hr_employee_portfolio_group;


INSERT INTO hr_employee_portfolio_group (GROUP_name)
VALUES
('Trust Governance_Taumata Advisor Portfolio'), 
('Trust Corporate Portfolio'), 
('Trust Operations Management Portfolio')

/*
UPDATE hr_employee_portfolio_group SET group_name = 'Trust Governance_Taumata Advisor Portfolio' WHERE id = 1;
UPDATE hr_employee_portfolio_group SET group_name = 'Trust Corporate Portfolio' WHERE id = 2;
UPDATE hr_employee_portfolio_group SET group_name = 'Trust Operations Management Portfolio' WHERE id = 3;
*/

INSERT INTO hr_employee_portfolio (group_id, portfolio)
VALUES (1, 'Health Advisors - Mental'),
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


