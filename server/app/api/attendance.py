from datetime import date, datetime, time, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from bson import ObjectId

from .. import crud, schemas, ml_model
from ..core.database import db
from ..core.security import get_current_active_user, get_current_admin
from ..utils.email_utils import send_fraud_alert

router = APIRouter()

@router.post("/mark-attendance", response_model=dict)
def mark_attendance(
    attendance: schemas.AttendanceCreate,
    request: Request,
    current_user: dict = Depends(get_current_active_user),
):
    # Verify class exists
    class_ = crud.get_class(str(attendance.class_id))
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if class is scheduled for current week and day (monthly schedule)
    current_datetime = datetime.now()
    current_weekday = current_datetime.weekday()  # 0=Monday, 6=Sunday
    
    # Calculate current week of the month (1-5)
    first_day_of_month = current_datetime.replace(day=1)
    current_week_of_month = ((current_datetime.day - 1) // 7) + 1
    
    class_day = class_.get('day_of_week')
    class_week = class_.get('week_number')
    
    # Only validate schedule if both day and week are set
    if class_day is not None and class_week is not None:
        if current_weekday != class_day:
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            raise HTTPException(status_code=400, detail=f"This class is scheduled for {day_names[class_day]} only")
        
        if current_week_of_month != class_week:
            raise HTTPException(status_code=400, detail=f"This class is scheduled for week {class_week} of the month only. Current week: {current_week_of_month}")
    
    # Check if attendance is within class time ±30 minutes
    # Use local time (from frontend) instead of UTC
    current_time = current_datetime.time()
    schedule_time_str = class_.get('schedule_time')
    if schedule_time_str:
        try:
            # Try parsing both formats: HH:MM:SS and HH:MM
            try:
                schedule_time = datetime.strptime(schedule_time_str, '%H:%M:%S').time()
            except ValueError:
                schedule_time = datetime.strptime(schedule_time_str, '%H:%M').time()
            
            schedule_datetime = datetime.combine(current_datetime.date(), schedule_time)
            start_time = (schedule_datetime - timedelta(minutes=30)).time()
            end_time = (schedule_datetime + timedelta(minutes=30)).time()
            
            if not (start_time <= current_time <= end_time):
                raise HTTPException(status_code=400, detail=f"Attendance can only be marked from {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}. Current time: {current_time.strftime('%H:%M:%S')}")
        except HTTPException:
            raise
        except Exception as e:
            # Log the error but allow attendance if time parsing fails
            print(f"Warning: Could not parse schedule_time '{schedule_time_str}': {str(e)}")
            # Allow attendance if time parsing fails (backward compatibility)
    
    # Convert user ID to string for consistency
    user_id = str(current_user["_id"]) if isinstance(current_user["_id"], ObjectId) else current_user["_id"]
    class_id = str(attendance.class_id)
    
    # Check for duplicate attendance
    duplicate = crud.check_duplicate_attendance(user_id, class_id, attendance.device_id)
    if duplicate:
        raise HTTPException(status_code=400, detail="Attendance already marked for this class today")
    
    # Check geo-fencing
    if not ml_model.is_within_campus(attendance.latitude, attendance.longitude):
        raise HTTPException(status_code=403, detail="Attendance can only be marked within campus boundaries")
    
    ip_address = request.client.host if request.client else "unknown"
    fraud_score, is_flagged, fraud_reasons = ml_model.analyze_attendance(
        db,
        user_id,
        datetime.utcnow(),
        attendance.latitude,
        attendance.longitude,
        attendance.device_id,
    )
    
    # Send email alert if fraud detected
    if is_flagged:
        send_fraud_alert(current_user["email"], fraud_score, fraud_reasons)
    
    entry = crud.create_attendance(
        user_id,
        class_id,
        {"latitude": attendance.latitude, "longitude": attendance.longitude, "device_id": attendance.device_id},
        ip_address,
        fraud_score,
        is_flagged,
        fraud_reasons
    )
    return entry

@router.get("/get-attendance", response_model=list[dict])
def get_attendance(
    student: str = None,
    date_param: date = None,
    fraud_score_min: int = None,
    current_user: dict = Depends(get_current_active_user),
):
    if current_user.get("role") == "student":
        return crud.get_attendance_for_user(current_user["_id"])
    return crud.get_attendance_records(student, date_param, fraud_score_min)

def _get_week_of_month_and_bounds(current_datetime: datetime):
    current_week_of_month = ((current_datetime.day - 1) // 7) + 1
    first_day_of_month = current_datetime.replace(day=1)
    week_start = first_day_of_month + timedelta(days=(current_week_of_month - 1) * 7)
    week_start = week_start - timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=6)
    return current_week_of_month, week_start, week_end


def _attendance_exists(user_id: str, class_id: str, target_date: date):
    return db.attendances.find_one({
        'user_id': user_id,
        'class_id': class_id,
        'timestamp': {
            '$gte': datetime.combine(target_date, datetime.min.time()),
            '$lt': datetime.combine(target_date + timedelta(days=1), datetime.min.time())
        }
    }) is not None


@router.get("/student-weekly-attendance", response_model=dict)
def get_student_weekly_attendance(
    current_user: dict = Depends(get_current_active_user),
):
    """Get student's weekly timetable and attendance summary"""
    user_id = str(current_user["_id"]) if isinstance(current_user["_id"], ObjectId) else current_user["_id"]
    current_datetime = datetime.now()
    current_week_of_month, week_start, week_end = _get_week_of_month_and_bounds(current_datetime)

    all_classes = crud.get_all_classes()
    week_schedule = [{
        'day_of_week': day,
        'date': (week_start + timedelta(days=day)).strftime('%Y-%m-%d'),
        'day_name': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day],
        'classes': []
    } for day in range(7)]

    subject_summary = {}
    total_classes = 0
    total_attended = 0

    for class_obj in all_classes:
        class_week = class_obj.get('week_number')
        class_day = class_obj.get('day_of_week')
        if class_day is None:
            continue
        if class_week is not None and class_week != current_week_of_month:
            continue

        class_date = week_start + timedelta(days=class_day)
        attended = _attendance_exists(user_id, str(class_obj['_id']), class_date)

        class_data = {
            'class_id': class_obj['_id'],
            'name': class_obj['name'],
            'subject': class_obj.get('subject', {}),
            'schedule_time': class_obj.get('schedule_time'),
            'room_number': class_obj.get('room_number'),
            'day_of_week': class_day,
            'week_number': class_week,
            'date': class_date.strftime('%Y-%m-%d'),
            'attended': attended
        }

        week_schedule[class_day]['classes'].append(class_data)

        subject_name = class_data['subject'].get('name', 'Unknown Subject')
        subject_code = class_data['subject'].get('code', 'UNK')
        if subject_name not in subject_summary:
            subject_summary[subject_name] = {
                'subject_code': subject_code,
                'classes': [],
                'total_classes': 0,
                'attended_classes': 0,
                'percentage': 0
            }

        subject_summary[subject_name]['classes'].append(class_data)
        subject_summary[subject_name]['total_classes'] += 1
        if attended:
            subject_summary[subject_name]['attended_classes'] += 1
        total_classes += 1
        if attended:
            total_attended += 1

    for summary in subject_summary.values():
        summary['percentage'] = round((summary['attended_classes'] / summary['total_classes']) * 100, 1) if summary['total_classes'] > 0 else 0

    return {
        'week_of_month': current_week_of_month,
        'month': current_datetime.strftime('%B %Y'),
        'week_start': week_start.strftime('%Y-%m-%d'),
        'week_end': week_end.strftime('%Y-%m-%d'),
        'total_classes': total_classes,
        'total_attended': total_attended,
        'weekly_percentage': round((total_attended / total_classes) * 100, 1) if total_classes > 0 else 0,
        'days': week_schedule,
        'subjects': subject_summary
    }


@router.get("/student-overall-attendance", response_model=dict)
def get_student_overall_attendance(
    current_user: dict = Depends(get_current_active_user),
):
    """Get student's overall attendance percentage"""
    user_id = str(current_user["_id"]) if isinstance(current_user["_id"], ObjectId) else current_user["_id"]
    attendance_records = crud.get_attendance_for_user(user_id)
    subject_stats = {}
    total_attended = len(attendance_records)
    total_possible = 0
    current_datetime = datetime.now()
    current_week_of_month, _, _ = _get_week_of_month_and_bounds(current_datetime)

    all_classes = crud.get_all_classes()
    for class_obj in all_classes:
        subject = class_obj.get('subject', {})
        subject_name = subject.get('name', 'Unknown Subject')
        subject_code = subject.get('code', 'UNK')
        if subject_name not in subject_stats:
            subject_stats[subject_name] = {
                'subject_code': subject_code,
                'attended': 0,
                'total_possible': 0,
                'percentage': 0
            }

        class_week = class_obj.get('week_number')
        if class_week is None or class_week <= current_week_of_month:
            subject_stats[subject_name]['total_possible'] += 1
            total_possible += 1
            if any(a['class_id'] == class_obj['_id'] for a in attendance_records):
                subject_stats[subject_name]['attended'] += 1

    for summary in subject_stats.values():
        summary['percentage'] = round((summary['attended'] / summary['total_possible']) * 100, 1) if summary['total_possible'] > 0 else 0

    overall_percentage = round((total_attended / total_possible) * 100, 1) if total_possible > 0 else 0
    return {
        'overall_percentage': overall_percentage,
        'total_attended': total_attended,
        'total_possible': total_possible,
        'subjects': subject_stats,
        'at_risk': overall_percentage < 50
    }

@router.get("/admin-student-attendance", response_model=list[dict])
def get_admin_student_attendance(
    current_user: dict = Depends(get_current_admin),
):
    """Get attendance overview for all students (admin/teacher view)"""
    students = list(db.users.find({"role": "student"}))
    student_attendance = []
    current_datetime = datetime.now()
    current_week_of_month = ((current_datetime.day - 1) // 7) + 1

    all_classes = crud.get_all_classes()
    scheduled_classes = [
        class_obj for class_obj in all_classes
        if class_obj.get('day_of_week') is not None and class_obj.get('week_number') is not None
    ]
    total_possible = len(scheduled_classes)

    first_day_of_month = current_datetime.replace(day=1)
    week_start_offset = (current_week_of_month - 1) * 7
    week_start = first_day_of_month + timedelta(days=week_start_offset)
    week_start = week_start - timedelta(days=week_start.weekday())

    for student in students:
        student_id = str(student["_id"])
        attendance_records = crud.get_attendance_for_user(student_id)
        attended_class_ids = {att['class_id'] for att in attendance_records}
        flagged_attendances = [att for att in attendance_records if att.get('is_flagged')]

        total_attended = sum(
            1 for class_obj in scheduled_classes
            if str(class_obj['_id']) in attended_class_ids
        )
        overall_percentage = round((total_attended / total_possible) * 100, 1) if total_possible > 0 else 0

        weekly_stats = {}
        weekly_total = 0
        weekly_attended = 0

        for class_obj in scheduled_classes:
            if class_obj.get('week_number') != current_week_of_month:
                continue

            subject = class_obj.get('subject', {})
            subject_name = subject.get('name', 'Unknown')
            weekly_stats.setdefault(subject_name, {'attended': 0, 'total': 0, 'percentage': 0})
            weekly_stats[subject_name]['total'] += 1
            weekly_total += 1

            class_date = week_start + timedelta(days=class_obj.get('day_of_week'))
            attendance_record = db.attendances.find_one({
                'user_id': student_id,
                'class_id': str(class_obj['_id']),
                'timestamp': {
                    '$gte': datetime.combine(class_date, datetime.min.time()),
                    '$lt': datetime.combine(class_date + timedelta(days=1), datetime.min.time())
                }
            })
            if attendance_record:
                weekly_stats[subject_name]['attended'] += 1
                weekly_attended += 1

        for summary in weekly_stats.values():
            summary['percentage'] = round((summary['attended'] / summary['total']) * 100, 1) if summary['total'] > 0 else 0

        student_attendance.append({
            'student_id': student_id,
            'student_email': student['email'],
            'overall_percentage': overall_percentage,
            'total_attended': total_attended,
            'total_possible': total_possible,
            'weekly_percentage': round((weekly_attended / weekly_total) * 100, 1) if weekly_total > 0 else 0,
            'current_week_of_month': current_week_of_month,
            'month': current_datetime.strftime('%B %Y'),
            'weekly_subjects': weekly_stats,
            'flagged_attendances': len(flagged_attendances),
            'at_risk': overall_percentage < 50
        })

    return student_attendance