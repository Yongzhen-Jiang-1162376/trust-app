from typing import Literal
from app.extensions import db
from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, func, ForeignKey, Integer, Float, String, Text, DateTime, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

GenderType = Literal['Female', 'Male']
EmployeeType = Literal['Employee', 'Volunteer']
WorkModeTpye = Literal['Onsite', 'Remote', 'Hybrid']


class Employee(db.Model):
    __tablename__ = 'hr_employee'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_date: Mapped[Optional[date]]
    full_name: Mapped[str] = mapped_column(String(255))
    gender: Mapped[GenderType]
    trial_period_start_date: Mapped[Optional[date]]
    employee_type: Mapped[EmployeeType]
    position: Mapped[Optional[str]] = mapped_column(String(255))
    mode_of_work: Mapped[WorkModeTpye]
    volunteer_current_status: Mapped[Optional[str]] = mapped_column(String(255))
    hours_per_week: Mapped[Optional[str]] = mapped_column(String(255))
    portfolio_assigned: Mapped[Optional[str]] = mapped_column(String(255))
    manager_name: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    date_of_birth: Mapped[Optional[date]]
    nationality: Mapped[Optional[str]] = mapped_column(String(255))
    contact_detail: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    trial_period: Mapped[Optional[str]] = mapped_column(String(255))
    resignation_date: Mapped[Optional[date]]
    last_working_date: Mapped[Optional[date]]
    feedback_performance_review: Mapped[Optional[str]] = mapped_column(Text)
    # leave_reason_id: Mapped[Optional[int]] = mapped_column(ForeignKey('hr_leave_reason.id'))
    leave_reason: Mapped[Optional[str]] = mapped_column(String(255))
    comments: Mapped[Optional[str]] = mapped_column(String(255))
    documents: Mapped[list['EmployeeDocument']] = relationship()
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, insert_default=func.now())
    created_by_id: Mapped[Optional[int]]
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now())
    updated_by_id: Mapped[Optional[int]]
    
    def __repr__(self):
        return f'<Employee {self.fullname}>'


# class LeaveReason(db.Model):
#     __tablename__ = 'hr_leave_reason'
    
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     reason: Mapped[str] = mapped_column(String(255), unique=True)
#     created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, insert_default=func.now())
#     created_by_id: Mapped[Optional[int]]
#     updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now())
#     updated_by_id: Mapped[Optional[int]]
    
#     def __repr__(self):
#         return f'<LeaveReason {self.reason}>'


class EmployeeDocument(db.Model):
    __tablename__ = 'hr_employee_document'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('hr_employee.id'))
    original_file_name: Mapped[str] = mapped_column(Text)
    extension: Mapped[str] = mapped_column(String(255))
    file_uuid: Mapped[str] = mapped_column(String(36))
    file_name: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, insert_default=func.now())
    created_by_id: Mapped[Optional[int]]
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now())
    updated_by_id: Mapped[Optional[int]]


class EmployeePortfolioGroup(db.Model):
    __tablename__ = 'hr_employee_portfolio_group'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(255))


class EmployeePortfolio(db.Model):
    __tablename__ = 'hr_employee_portfolio'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('hr_employee_portfolio_group.id'))
    portfolio: Mapped[str] = mapped_column(String(255))


class EmployeePortfolioAssigned(db.Model):
    __tablename__ = 'hr_employee_portfolio_assigned'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('hr_employee.id'))
    portfolio_id: Mapped[int] = mapped_column(ForeignKey('hr_employee_portfolio.id'))
