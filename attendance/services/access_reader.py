import pyodbc
import sys
from django.utils import timezone
from django.utils.timezone import make_aware
from attendance.models import Student, AttendanceLog, DefaultClockOutReason

print(sys.path)
print("Module path:", __name__)

ACCESS_DB_PATH = r"D:\elburgon_attendance\att2000.mdb"  # Update path if needed

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

            # Generate unique ID
            unique_id = f"{admission_number}_{timestamp.isoformat()}_{status}"

            # Skip if log already exists by unique_id
            if AttendanceLog.objects.filter(unique_id=unique_id).exists():
                continue

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
            continue  # Skip unregistered students

    conn.close()
    return count
