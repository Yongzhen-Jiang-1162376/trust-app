from marshmallow import Schema, fields


class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    start_date = fields.Date()
    full_name = fields.Str(required=True)
    gender = fields.Str()
    trial_period_start_date = fields.Date()
    employee_type = fields.Str()
    position = fields.Str()
    mode_of_work = fields.Str()
    volunteer_current_status = fields.Str()
    hours_per_week = fields.Float()
    portfolio_assigned = fields.Str()
    manager_name = fields.Str()
    address = fields.Str()
    date_of_birth = fields.Date()
    nationality = fields.Str()
    contact_detail = fields.Str()
    email = fields.Str()
    trial_period = fields.Float()
    resignation_date = fields.Date()
    last_working_date = fields.Date()
    feedback_performance_review = fields.Str()
    leave_reason_id = fields.Int()
    leave_reason = fields.Str()
    comments = fields.Str()


class LeaveReasonSchema(Schema):
    id = fields.Int(dump_only=True)
    reason = fields.Str(required=True)
