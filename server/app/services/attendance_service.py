from datetime import datetime
from sqlalchemy.orm import Session

import crud
import ml_model
from models.attendance import Attendance
from schemas.attendance_schema import AttendanceCreate

class AttendanceService:
    def __init__(self, db: Session):
        self.db = db

    def mark_attendance(self, user_id: int, attendance_data: AttendanceCreate, ip_address: str):
        fraud_score, is_flagged = ml_model.analyze_attendance(
            self.db,
            datetime.utcnow(),
            attendance_data.latitude,
            attendance_data.longitude,
            attendance_data.device_id,
        )
        entry = crud.create_attendance(self.db, user_id, attendance_data, ip_address, fraud_score, is_flagged)

        # Retrain model if we have enough data
        if self.db.query(Attendance).count() >= 20:
            ml_model.train_model(self.db)

        return entry

    def get_user_attendance(self, user_id: int):
        return crud.get_attendance_for_user(self.db, user_id)

    def get_all_attendance(self, student_id=None, date=None, fraud_score_min=None):
        return crud.get_attendance_records(self.db, student_id, date, fraud_score_min)

    def get_fraud_analysis(self):
        flagged = crud.get_flagged_entries(self.db)
        total = crud.count_attendance(self.db)
        return {"flagged": flagged, "total_records": total}