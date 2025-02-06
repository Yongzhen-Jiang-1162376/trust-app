from sqlalchemy import Column, func, ForeignKey, Integer, String, DateTime, Boolean, text, Table
from app.extensions import Base

user_portfolio_association = Table(
    'auth_user_portfolio',
    Base.metadata,
    Column('user_id', ForeignKey('auth_user.id'), primary_key=True),
    Column('portfolio_id', ForeignKey('hr_employee_portfolio.id'), primary_key=True)
)