import crud

class FraudService:
    def __init__(self, db):
        self.db = db

    def get_fraud_stats(self):
        """Get fraud statistics for admin dashboard"""
        total_records = crud.count_attendance(self.db)
        flagged_records = len(crud.get_flagged_entries(self.db))

        return {
            "total_records": total_records,
            "flagged_records": flagged_records,
            "normal_records": total_records - flagged_records,
            "fraud_percentage": round((flagged_records / total_records * 100) if total_records > 0 else 0, 2)
        }

    def get_fraud_alerts(self, limit: int = 10):
        """Get recent fraud alerts"""
        return crud.get_flagged_entries(self.db)[:limit]

    def get_suspicious_patterns(self):
        """Analyze patterns in fraudulent attendance"""
        flagged_entries = crud.get_flagged_entries(self.db)

        patterns = {
            "high_score_entries": len([e for e in flagged_entries if e.fraud_score > 80]),
            "location_anomalies": len([e for e in flagged_entries if not e.latitude or not e.longitude]),
            "device_switches": len(set([e.device_id for e in flagged_entries if e.device_id])),
        }

        return patterns