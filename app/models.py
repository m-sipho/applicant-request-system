from sqlalchemy import Column, Integer, String, Enum, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from .database import Base
from .request_types import RequestType
from .schemas import StatusEnum, RoleEnum
from sqlalchemy.orm import relationship

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(RequestType), nullable=False)
    description = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.SUBMITTED, nullable=False)
    data = Column(JSON, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", foreign_keys=[owner_id], back_populates="requests")
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="assigned_requests")

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