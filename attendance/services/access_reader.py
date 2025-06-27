import pyodbc
import datetime
from django.utils import timezone
from django.utils.timezone import make_aware
from attendance.models import Student, AttendanceLog
import sys
print(sys.path)
print("Module path:", __name__)

ACCESS_DB_PATH = r"D:\elburgon_attendance\att2000.mdb"  # Adjusted path

def fetch_access_logs():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        rf'DBQ={ACCESS_DB_PATH};'
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Join CHECKINOUT with USERINFO using USERID to get Badgenumber
    cursor.execute("""
        SELECT U.Badgenumber, C.CHECKTIME, C.CHECKTYPE
        FROM CHECKINOUT C
        INNER JOIN USERINFO U ON C.USERID = U.USERID
    """)

    count = 0
    for row in cursor.fetchall():
        admission_number = str(row.Badgenumber).strip()
        timestamp = make_aware(row.CHECKTIME)
        status = 'IN' if row.CHECKTYPE.upper() == 'I' else 'OUT'

        try:
            student = Student.objects.get(admission_number=admission_number)

            # Avoid duplicate logs
            if not AttendanceLog.objects.filter(student=student, timestamp=timestamp, status=status).exists():
                AttendanceLog.objects.create(
                    student=student,
                    timestamp=timezone.make_aware(timestamp),
                    status=status,
                    reason=''  # Default reason blank
                )
                count += 1

        except Student.DoesNotExist:
            # Log or skip if no student found
            continue

    conn.close()
    return count
