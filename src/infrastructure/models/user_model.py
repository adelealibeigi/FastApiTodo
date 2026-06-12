from sqlalchemy import Column, DateTime, String, Integer, Boolean, func
from sqlalchemy.orm import relationship

from src.infrastructure.config import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    username = Column('UserName', String(250), nullable=False, unique=True)
    password = Column('Password', String, nullable=False)
    phone_number = Column('PhoneNumber', String(11), nullable=True)
    email = Column('Email', String, nullable=False)
    is_active = Column('IsActive', Boolean, default=True)
    created_date = Column('CreatedDate', DateTime, server_default=func.now())
    updated_date = Column('UpdatedDate', DateTime, server_default=func.now(), server_onupdate=func.now())
    tasks = relationship("TaskModel", back_populates="user")
