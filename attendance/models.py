import datetime
from django.db import models

class Student(models.Model):
    admission_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    class_name = models.CharField(max_length=50, blank=True)  # e.g., "Form 1", "Grade 9"
    entry_year = models.PositiveIntegerField(null=True, blank=True)  # e.g., 2022
    education_cycle = models.PositiveSmallIntegerField(default=4)  # 4 or 3 years
    is_active = models.BooleanField(default=True)

    def expected_graduation_year(self):
        if self.entry_year and self.education_cycle:
            return self.entry_year + self.education_cycle
        return None

    def has_graduated(self, current_year=None):
        current_year = current_year or datetime.datetime.now().year
        return self.expected_graduation_year() and current_year >= self.expected_graduation_year()

    def __str__(self):
        return f"{self.full_name} ({self.admission_number})"


class AttendanceLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=[('IN', 'Clock In'), ('OUT', 'Clock Out')]
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Required for Clock Out: e.g., Health, Fees, Holiday, Discipline"
    )
    synced = models.BooleanField(default=False)  # Has SMS been sent?

    def __str__(self):
        return f"{self.student} - {self.status} @ {self.timestamp}"
