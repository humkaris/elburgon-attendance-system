import pyodbc
import datetime
import sys
from django.utils import timezone
from django.utils.timezone import make_aware
from attendance.models import Student, AttendanceLog, DefaultClockOutReason

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
        timestamp = row.CHECKTIME
        if not timezone.is_aware(timestamp):
            timestamp = make_aware(timestamp)

        status = 'in' if row.CHECKTYPE.upper() == 'I' else 'out'

        try:
            student = Student.objects.get(admission_number=admission_number)

            # Create a unique identifier per log
            unique_id = f"{student.admission_number}_{timestamp.isoformat()}_{status}"

            # Avoid duplicate logs using unique_id
            if not AttendanceLog.objects.filter(unique_id=unique_id).exists():
                # Apply default clock-out reason if applicable
                reason = None
                if status == 'out':
                    default = DefaultClockOutReason.objects.filter(date=timestamp.date()).first()
                    if default:
                        reason = default.reason

                AttendanceLog.objects.create(
                    student=student,
                    timestamp=timestamp,
                    status=status,
                    reason=reason,
                    unique_id=unique_id
                )
                count += 1

        except Student.DoesNotExist:
            continue  # Ignore unknown badge numbers

    conn.close()
    return count
