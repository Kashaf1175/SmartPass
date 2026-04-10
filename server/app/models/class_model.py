import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship

from ..core.database import Base

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    schedule_time = Column(Time, nullable=True)  # Class start time
    room_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    subject = relationship("Subject", back_populates="classes")
    attendances = relationship("Attendance", back_populates="class_")
