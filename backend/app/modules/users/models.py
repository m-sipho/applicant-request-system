from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from schemas import RoleEnum
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    requests = relationship("Request", foreign_keys="Request.owner_id", back_populates="owner")
    assigned_requests = relationship("Request", foreign_keys="Request.assignee_id", back_populates="assignee")