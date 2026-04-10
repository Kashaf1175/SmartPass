from typing import Optional
from pydantic import BaseModel

class SubjectCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class SubjectOut(BaseModel):
    _id: Optional[str] = None
    name: str
    code: str
    description: Optional[str] = None

    class Config:
        populate_by_name = True

class ClassCreate(BaseModel):
    name: str
    subject_id: str
    schedule_time: Optional[str] = None
    room_number: Optional[str] = None
    day_of_week: Optional[int] = None  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    week_number: Optional[int] = None  # Week number in semester (1-16)

class ClassOut(BaseModel):
    _id: Optional[str] = None
    name: str
    subject_id: str
    schedule_time: Optional[str] = None
    room_number: Optional[str] = None
    day_of_week: Optional[int] = None
    week_number: Optional[int] = None

    class Config:
        populate_by_name = True

class ClassWithSubject(BaseModel):
    _id: Optional[str] = None
    name: str
    subject: SubjectOut
    subject_id: Optional[str] = None
    schedule_time: Optional[str] = None
    room_number: Optional[str] = None
    day_of_week: Optional[int] = None
    week_number: Optional[int] = None

    class Config:
        populate_by_name = True
