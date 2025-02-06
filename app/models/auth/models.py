from app.extensions import db
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, func, ForeignKey, Integer, String, DateTime, Boolean, text, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import false, true
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app.extensions import Base
# from app.models.hr import EmployeePortfolio
from app.models.association import user_portfolio_association


class User(UserMixin, db.Model):
    __tablename__ = 'auth_user'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255))
    # username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    is_superadmin: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("0"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("1"))
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("0"))
    
    portfolios: Mapped[list['hr_employee_portfolio']] = relationship("EmployeePortfolio", secondary=user_portfolio_association, back_populates="users")
    
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now())
    created_by_id = mapped_column(Integer, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now())
    updated_by_id: Mapped[Optional[int]]

    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
