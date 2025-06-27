from django.core.management.base import BaseCommand
from attendance.services.access_reader import fetch_access_logs

class Command(BaseCommand):
    help = "Sync attendance data from Access DB"

    def handle(self, *args, **options):
        count = fetch_access_logs()
        self.stdout.write(self.style.SUCCESS(f"Imported {count} new attendance logs"))
