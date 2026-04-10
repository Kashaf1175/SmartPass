#!/usr/bin/env python3
"""
Update classes with monthly scheduling data for testing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import db
from datetime import datetime

def update_classes_with_scheduling():
    print("📅 Updating classes with monthly scheduling...")

    # Get current week of month
    current_datetime = datetime.now()
    current_week_of_month = ((current_datetime.day - 1) // 7) + 1

    # Update classes with scheduling data
    classes = list(db.classes.find({}))

    scheduling_data = [
        {"day_of_week": 0, "week_number": current_week_of_month},  # Monday, current week of month
        {"day_of_week": 2, "week_number": current_week_of_month},  # Wednesday, current week of month
        {"day_of_week": 1, "week_number": current_week_of_month},  # Tuesday, current week of month
        {"day_of_week": 3, "week_number": current_week_of_month},  # Thursday, current week of month
        {"day_of_week": 4, "week_number": current_week_of_month},  # Friday, current week of month
        {"day_of_week": 1, "week_number": current_week_of_month},  # Tuesday, current week of month
    ]

    for i, class_obj in enumerate(classes):
        if i < len(scheduling_data):
            db.classes.update_one(
                {"_id": class_obj["_id"]},
                {"$set": scheduling_data[i]}
            )
            print(f"  ✓ Updated {class_obj['name']} with day_of_week={scheduling_data[i]['day_of_week']}, week_number={scheduling_data[i]['week_number']}")

    print(f"\n✅ Classes updated successfully! Current week of month: {current_week_of_month}")
    print("📋 Classes are now scheduled for the current week of the month.")

if __name__ == "__main__":
    try:
        update_classes_with_scheduling()
    except Exception as e:
        print(f"❌ Error updating classes: {e}")
        sys.exit(1)