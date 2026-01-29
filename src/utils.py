import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "attendance.csv")

def mark_attendance(name, status):
    file_exists = os.path.isfile(CSV_PATH)

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Status", "Timestamp"])

        writer.writerow([name, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
