/*
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
*/


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
'Edith Corona',
'Female',
'Software Developer',
'Business Analysis Management Portfolio',
'Tracy',
'Employee',
'Onsite',
'1983-01-03',
'New Zealand',
'john.smith@gmail.com',
'+64-027-1234-9876',
'102 East Rd, Christchurch',
'2023-09-01',
'2024-09-01',
'2024-12-31',
3,
'2024-09-08',
40,
'Working',
'John is excellent',
1,
'This is a comment'
),
(
'Lillian Heath',
'Female',
'Software Developer',
'Business Analysis Management Portfolio',
'Tracy',
'Employee',
'Onsite',
'1983-01-03',
'New Zealand',
'john.smith@gmail.com',
'+64-027-1234-9876',
'102 East Rd, Christchurch',
'2023-09-01',
'2024-09-01',
'2024-12-31',
3,
'2024-09-08',
40,
'Working',
'John is excellent',
1,
'This is a comment'
),
(
'Jason Wu',
'Female',
'Software Developer',
'Business Analysis Management Portfolio',
'Tracy',
'Employee',
'Onsite',
'1983-01-03',
'New Zealand',
'john.smith@gmail.com',
'+64-027-1234-9876',
'102 East Rd, Christchurch',
'2023-09-01',
'2024-09-01',
'2024-12-31',
3,
'2024-09-08',
40,
'Working',
'John is excellent',
1,
'This is a comment'
),
(
'Etta Magana',
'Female',
'Software Developer',
'Business Analysis Management Portfolio',
'Tracy',
'Employee',
'Onsite',
'1983-01-03',
'New Zealand',
'john.smith@gmail.com',
'+64-027-1234-9876',
'102 East Rd, Christchurch',
'2023-09-01',
'2024-09-01',
'2024-12-31',
3,
'2024-09-08',
40,
'Working',
'John is excellent',
1,
'This is a comment'
)


UPDATE hr_employee
SET trial_period_start_date = '2023-03-15',
	 comments = 'This is another comment'
WHERE id = 2


UPDATE hr_employee
SET start_date = '2024-04-01',
	 resignation_date = '2024-12-01',
	 last_working_date = '2024-12-31',
	 volunteer_current_status = 'working'


UPDATE hr_employee
SET address = contact_detail

UPDATE hr_employee
SET contact_detail = '+64-027-3764-1221'



SELECT
	e.id,
	e.full_name,
	e.gender,
	e.position,
   e.portfolio_assigned,
   e.manager_name,
   e.employee_type,
   e.mode_of_work,
   e.date_of_birth,
   e.nationality,
   e.email,
   e.contact_detail,
   e.address,
   e.start_date,
   e.resignation_date,
   e.last_working_date,
   e.trial_period,
   e.trial_period_start_date,
   e.hours_per_week,
   e.volunteer_current_status,
   e.feedback_performance_review,
   e.leave_reason_id,
   l.reason AS leave_reason,
   e.comments
FROM hr_employee e
LEFT JOIN hr_leave_reason l ON e.leave_reason_id = l.id



SELECT start_date FROM hr_employee

SELECT
	id,
	employee_id,
	original_file_name,
	extension,
	file_uuid,
	date_format(created_at, '%Y-%m-%d %H:%i:%s') AS created_at
FROM hr_employee_document;


SELECT * FROM alembic_version
