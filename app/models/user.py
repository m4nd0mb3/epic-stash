"""
Models Module
"""

# pylint: disable=R0903,E0401,C0103
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship  # , declarative_settings.DBBaseModel


# from app.core.config import settings
from app.models.base import BaseModel

# Base = declarative_base()


class UserModel(BaseModel):
    """
    User Model Class
    """

    __tablename__ = "users"

    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True, unique=True)
    password = Column(String(256), nullable=False)
    avatar = Column(String)
    is_staff = Column(Boolean, default=False)

    # roles = relationship("RoleModel")
    # roles = relationship("RoleModel", back_populates="user")
    # closed_sales_box = relationship("UserModel", back_populates="closed_user")
    # opened_sales_box = relationship("UserModel", back_populates="opened_user")
