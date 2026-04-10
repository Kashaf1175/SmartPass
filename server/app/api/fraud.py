from fastapi import APIRouter, Depends

from .. import crud
from ..core.security import get_current_admin

router = APIRouter()

@router.get("/fraud-stats", response_model=dict)
def get_fraud_stats(current_user: dict = Depends(get_current_admin)):
    """Get fraud statistics for admin dashboard"""
    flagged_entries = crud.get_flagged_entries()
    total_records = crud.count_attendance()

    return {
        "total_records": total_records,
        "flagged": flagged_entries,
    }

@router.get("/fraud-alerts", response_model=list[dict])
def get_fraud_alerts(limit: int = 10, current_user: dict = Depends(get_current_admin)):
    """Get recent fraud alerts"""
    flagged = crud.get_flagged_entries()
    return flagged[:limit]