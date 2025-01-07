SELECT * FROM employee;

INSERT INTO employee (
NAME, 
START_date, 
trial_period_start_date, 
gender, 
employment_status, 
employee_type, 
POSITION, 
mode_of_work,
volunteer_current_status, 
hours_per_week, 
portfolio_assigned, 
manager_name, 
address, 
date_of_birth, 
nationality, 
contact_detail, 
email,
comments, 
trial_period, 
resignation_date, 
last_working_day, 
feedback_performance_review, 
reason_for_leaving)
VALUES
(
'Trump Donald', 
'2024-09-10', 
'2023-12-01', 
'M', 
2, 
'Employee', 
'Engineer', 
'Remote', 
'Active', 
40, 
'Policy Analyst Researcher Management Portfolio ', 
'Tracy',
'32 East Rd, Wellington', 
'1985-10-01', 
'United States', 
'+64-023-12345678', 
'trump.donald@gmail.com', 
'this is a comment', 
3, 
'2025-01-31', 
'2025-02-10',
'excellent performance', 
'personal reason'
)



SELECT * FROM employee_bak;

SELECT * FROM alembic_version;

SELECT * FROM auth_user;
SELECT * FROM hr_employee;
SELECT * FROM hr_employee_document;
SELECT * FROM hr_leave_reason;

SELECT
	a.fullname,
	a.gender,
	a.employee_type,
	a.`position`,
	b.filename,
	b.filepath
FROM hr_employee a
INNER JOIN hr_employee_document b ON a.id = b.employee_id


INSERT INTO hr_leave_reason (reason) VALUES ('Personal'), ('Family'), ('Relocation');



INSERT INTO hr_employee 
(
full_name, 
gender,
`position`,
portfolio_assigned,
manager_name,
employee_type,
mode_of_work,
date_of_birth,
nationality,
email,
contact_detail,
address,
start_date,
resignation_date,
last_working_date,
trial_period,
trial_period_start_date,
hours_per_week,
volunteer_current_status,
feedback_performance_review,
leave_reason_id,
comments
) VALUES
(
'John Smith',
'Male',
'Software Developer',
'Business Analysis Management Portfolio',
'Tracy',
'Employee',
'Onsite',
'1983-01-03',
'New Zealand',
'john.smith@gmail.com',
'102 East Rd, Christchurch',
'2023-09-01',
NULL,
NULL,
NULL,
3,
'2024-09-08',
40,
NULL,
'John is excellent',
1,
'This is a comment'
),
(
'Mary Smith',
'Female',
'Administrator',
'Marketing Management Portfolio',
'Trump',
'Employee',
'Remote',
'1987-09-03',
'New Zealand',
'marry.smith@gmail.com',
'200 Sumner Rd, Christchurch',
'2024-09-01',
NULL,
NULL,
NULL,
3,
'2024-03-15',
40,
NULL,
'Mary is excellent',
3,
'This is another comment'
)


UPDATE hr_employee
SET trial_period_start_date = '2023-03-15',
	 comments = 'This is another comment'
WHERE id = 2





