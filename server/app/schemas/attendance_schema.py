from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

class AttendanceCreate(BaseModel):
    class_id: str
    latitude: Optional[float]
    longitude: Optional[float]
    device_id: str

class AttendanceOut(BaseModel):
    _id: Optional[str] = None
    user_id: str
    class_id: str
    timestamp: datetime
    latitude: Optional[float]
    longitude: Optional[float]
    device_id: str
    ip_address: Optional[str]
    fraud_score: int
    is_flagged: bool

    class Config:
        populate_by_name = True

class AttendanceQuery(BaseModel):
    student: Optional[str] = None
    date: Optional[date] = None
    fraud_score_min: Optional[int] = None

class FraudResponse(BaseModel):
    flagged: List[AttendanceOut]
    total_records: int