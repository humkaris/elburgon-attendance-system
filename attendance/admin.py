from django.contrib import admin
from .models import Student, AttendanceLog, DefaultClockOutReason

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'full_name', 'parent_phone', 'is_active')

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'status', 'timestamp', 'reason', 'synced']
    list_filter = ['status', 'synced', 'reason']
    search_fields = ['student__full_name', 'student__admission_number']
    list_editable = ['reason', 'synced']  # Quick edit on list view

admin.site.register(DefaultClockOutReason)