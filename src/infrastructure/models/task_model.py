from sqlalchemy import (Column, DateTime, String, Integer, Text, func, ForeignKey, SmallInteger, Boolean)

from sqlalchemy.orm import relationship

from src.infrastructure.config import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    user_id = Column("UserId", Integer, ForeignKey("users.Id"))
    title = Column('Title', String(150), nullable=False)
    description = Column('Description', Text, nullable=True)
    due_date = Column('DueTime', DateTime, nullable=True)
    priority = Column('Priority', SmallInteger)
    status = Column('Status', SmallInteger)
    is_deleted = Column('IsDeleted', Boolean, default=False)
    deleted_at = Column('DeletedAt',DateTime, nullable=True)
    created_date = Column('CreatedDate', DateTime, server_default=func.now())
    updated_date = Column('UpdatedDate', DateTime, server_default=func.now(), server_onupdate=func.now())
    user = relationship("UserModel", back_populates="tasks", uselist=False)
