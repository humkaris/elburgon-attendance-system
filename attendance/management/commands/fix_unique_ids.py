from django.core.management.base import BaseCommand
from attendance.models import AttendanceLog
import hashlib

class Command(BaseCommand):
    help = 'Fix unique_id for AttendanceLog entries without one'

    def handle(self, *args, **kwargs):
        updated = 0

        logs = AttendanceLog.objects.filter(unique_id__isnull=True)
        for log in logs:
            base_string = f"{log.student.admission_number}|{log.timestamp.isoformat()}|{log.status}"
            unique_id = hashlib.sha256(base_string.encode()).hexdigest()

            # Ensure it's unique in DB just in case
            while AttendanceLog.objects.filter(unique_id=unique_id).exists():
                base_string += "X"  # Append something to change the hash
                unique_id = hashlib.sha256(base_string.encode()).hexdigest()

            log.unique_id = unique_id
            log.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Fixed unique_id for {updated} attendance logs."))
