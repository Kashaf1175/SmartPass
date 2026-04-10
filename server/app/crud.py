from datetime import datetime, date, timedelta
from bson import ObjectId
from .core.database import db

# User CRUD
def get_user_by_email(email: str):
    return db.users.find_one({"email": email})

def create_user(user_data: dict, hashed_password: str):
    user = {
        "email": user_data["email"],
        "hashed_password": hashed_password,
        "role": user_data.get("role", "student"),
        "created_at": datetime.utcnow()
    }
    result = db.users.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return user

# Subject CRUD
def create_subject(subject_data: dict):
    subject = {
        "name": subject_data["name"],
        "code": subject_data["code"],
        "description": subject_data.get("description"),
        "created_at": datetime.utcnow()
    }
    result = db.subjects.insert_one(subject)
    subject["_id"] = str(result.inserted_id)
    return subject

def get_subject(subject_id: str):
    subject = db.subjects.find_one({"_id": ObjectId(subject_id)})
    if subject:
        subject["_id"] = str(subject["_id"])
    return subject

def get_all_subjects():
    subjects = []
    for subject in db.subjects.find():
        subject["_id"] = str(subject["_id"])
        subjects.append(subject)
    return subjects

def delete_subject(subject_id: str):
    db.subjects.delete_one({"_id": ObjectId(subject_id)})

def update_subject(subject_id: str, subject_data: dict):
    """Update a subject"""
    update_data = {
        "name": subject_data.get("name"),
        "code": subject_data.get("code"),
        "description": subject_data.get("description"),
    }
    db.subjects.update_one({"_id": ObjectId(subject_id)}, {"$set": update_data})
    return get_subject(subject_id)

def get_subject_by_code(code: str):
    """Get subject by code"""
    return db.subjects.find_one({"code": code})

# Class CRUD
def create_class(class_data: dict):
    class_obj = {
        "name": class_data["name"],
        "subject_id": class_data["subject_id"],
        "schedule_time": class_data.get("schedule_time"),
        "room_number": class_data.get("room_number"),
        "day_of_week": class_data.get("day_of_week"),
        "week_number": class_data.get("week_number"),
        "created_at": datetime.utcnow()
    }
    result = db.classes.insert_one(class_obj)
    class_obj["_id"] = str(result.inserted_id)
    return class_obj

def get_class(class_id: str):
    class_obj = db.classes.find_one({"_id": ObjectId(class_id)})
    if class_obj:
        class_obj["_id"] = str(class_obj["_id"])
        # Get subject details
        subject = db.subjects.find_one({"_id": ObjectId(class_obj["subject_id"])})
        if subject:
            subject["_id"] = str(subject["_id"])
            class_obj["subject"] = subject
    return class_obj

def _normalize_object_id(value):
    return str(value) if isinstance(value, ObjectId) else value


def _enrich_class_subject(class_obj: dict):
    subject = None
    try:
        subject_id = class_obj.get("subject_id")
        if subject_id is not None:
            subject = db.subjects.find_one({"_id": ObjectId(subject_id)}) if isinstance(subject_id, str) else db.subjects.find_one({"_id": subject_id})
        if subject:
            subject["_id"] = str(subject["_id"])
            class_obj["subject"] = subject
    except Exception:
        pass
    return class_obj


def get_all_classes():
    classes = []
    for class_obj in db.classes.find():
        class_obj["_id"] = str(class_obj["_id"])
        class_obj["subject_id"] = str(class_obj.get("subject_id")) if class_obj.get("subject_id") is not None else None
        if class_obj.get("day_of_week") is not None:
            class_obj["day_of_week"] = int(class_obj["day_of_week"])
        if class_obj.get("week_number") is not None:
            class_obj["week_number"] = int(class_obj["week_number"])
        classes.append(_enrich_class_subject(class_obj))
    return classes


def get_weekly_timetable(week_of_month: int, year: int, month: int):
    week_start = date(year, month, 1) + timedelta(days=(week_of_month - 1) * 7)
    # Align to Monday for a clean weekly timetable view
    week_start = week_start - timedelta(days=week_start.weekday())
    week_days = [week_start + timedelta(days=i) for i in range(7)]

    schedule = {day: [] for day in range(7)}
    for class_obj in get_all_classes():
        if class_obj.get("day_of_week") is None:
            continue
        if class_obj.get("week_number") is not None and class_obj["week_number"] != week_of_month:
            continue

        class_date = week_days[class_obj["day_of_week"]]
        schedule[class_obj["day_of_week"]].append({
            "_id": class_obj["_id"],
            "name": class_obj["name"],
            "subject": class_obj.get("subject"),
            "schedule_time": class_obj.get("schedule_time"),
            "room_number": class_obj.get("room_number"),
            "day_of_week": class_obj.get("day_of_week"),
            "week_number": class_obj.get("week_number"),
            "date": class_date.strftime("%Y-%m-%d"),
        })

    return [{
        "day_of_week": day,
        "date": week_days[day].strftime("%Y-%m-%d"),
        "name": week_days[day].strftime("%A"),
        "classes": sorted(schedule[day], key=lambda item: item.get("schedule_time") or "")
    } for day in range(7)]


def get_classes_by_subject(subject_id: str):
    classes = []
    for class_obj in db.classes.find({"subject_id": subject_id}):
        class_obj["_id"] = str(class_obj["_id"])
        classes.append(class_obj)
    return classes

def delete_class(class_id: str):
    db.classes.delete_one({"_id": ObjectId(class_id)})

def update_class(class_id: str, class_data: dict):
    """Update a class"""
    update_data = {
        "name": class_data.get("name"),
        "subject_id": class_data.get("subject_id"),
        "schedule_time": class_data.get("schedule_time"),
        "room_number": class_data.get("room_number"),
    }
    db.classes.update_one({"_id": ObjectId(class_id)}, {"$set": update_data})
    return get_class(class_id)

# Attendance CRUD
def create_attendance(user_id: str, class_id: str, attendance_data: dict, ip_address: str, fraud_score: int, is_flagged: bool, fraud_reasons: list = None):
    # Ensure user_id and class_id are strings for consistency
    user_id_str = str(user_id) if isinstance(user_id, ObjectId) else user_id
    class_id_str = str(class_id) if isinstance(class_id, ObjectId) else class_id
    
    attendance = {
        "user_id": user_id_str,
        "class_id": class_id_str,
        "timestamp": datetime.utcnow(),
        "latitude": attendance_data.get("latitude"),
        "longitude": attendance_data.get("longitude"),
        "device_id": attendance_data["device_id"],
        "ip_address": ip_address,
        "fraud_score": fraud_score,
        "is_flagged": is_flagged,
        "fraud_reasons": fraud_reasons or [],
        "created_at": datetime.utcnow()
    }
    result = db.attendances.insert_one(attendance)
    attendance["_id"] = str(result.inserted_id)
    return attendance

def get_attendance_for_user(user_id: str):
    attendances = []
    user_id_str = str(user_id) if isinstance(user_id, ObjectId) else user_id
    for att in db.attendances.find({"user_id": user_id_str}).sort("timestamp", -1):
        att["_id"] = str(att["_id"])
        att["user_id"] = str(att["user_id"])
        att["class_id"] = str(att["class_id"])
        attendances.append(att)
    return attendances

def get_attendance_records(student_id: str = None, date_filter = None, fraud_score_min: int = None):
    query = {}
    if student_id:
        student_id_str = str(student_id) if isinstance(student_id, ObjectId) else student_id
        query["user_id"] = student_id_str
    if date_filter:
        query["timestamp"] = {
            "$gte": datetime.combine(date_filter, datetime.min.time()),
            "$lt": datetime.combine(date_filter + timedelta(days=1), datetime.min.time())
        }
    if fraud_score_min is not None:
        query["fraud_score"] = {"$gte": fraud_score_min}
    
    attendances = []
    for att in db.attendances.find(query).sort("timestamp", -1):
        att["_id"] = str(att["_id"])
        att["user_id"] = str(att["user_id"])
        att["class_id"] = str(att["class_id"])
        attendances.append(att)
    return attendances

def get_flagged_entries():
    flagged = []
    for att in db.attendances.find({"is_flagged": True}).sort("timestamp", -1):
        att["_id"] = str(att["_id"])
        att["user_id"] = str(att["user_id"])
        att["class_id"] = str(att["class_id"])
        flagged.append(att)
    return flagged

def count_attendance():
    return db.attendances.count_documents({})

def check_duplicate_attendance(user_id: str, class_id: str, device_id: str):
    """Check if student already marked attendance for this class today (regardless of device)"""
    # Ensure IDs are strings for consistent querying
    user_id_str = str(user_id) if isinstance(user_id, ObjectId) else user_id
    class_id_str = str(class_id) if isinstance(class_id, ObjectId) else class_id

    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Check for any attendance by this student for this class today (ignore device_id)
    return db.attendances.find_one({
        "user_id": user_id_str,
        "class_id": class_id_str,
        "timestamp": {
            "$gte": datetime.combine(today, datetime.min.time()),
            "$lt": datetime.combine(tomorrow, datetime.min.time())
        }
    })
