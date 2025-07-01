from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.models import AttendanceLog
from attendance.services.sms_sender import send_sms

class Command(BaseCommand):  # <--- THIS must be named exactly `Command`
    help = "Send SMS notifications for new attendance logs"

    def handle(self, *args, **kwargs):
        unsynced_logs = AttendanceLog.objects.filter(synced=False).select_related('student')
        sent_count = 0

        for log in unsynced_logs:
            student = log.student
            phone = student.parent_phone
            time_str = timezone.localtime(log.timestamp).strftime("%I:%M %p")
            date_str = timezone.localtime(log.timestamp).strftime("%d/%m/%Y")

            if log.status.lower() == 'out':
                reason_part = f" for {log.get_reason_display()}" if log.reason else ""
                message = (
                    f"Dear parent, your child {student.full_name} adm {student.admission_number} "
                    f"has left school{reason_part} on {date_str} at {time_str}. "
                    f"Elburgon Senior School"
                )
            else:
                message = (
                    f"Dear parent, your child {student.full_name} has arrived at school on "
                    f"{date_str} at {time_str}. Elburgon Senior School"
                )

            print(f"Sending to {phone}: {message}")
            success = send_sms(phone, message)

            if success:
                log.synced = True
                log.save()
                sent_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully sent {sent_count} messages."))
