from django.contrib import admin
from .models import Student, AttendanceLog, DefaultClockOutReason, SMSLog

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

@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ("student", "phone_number", "log_time", "sent_at", "success")
    list_filter = ("success", "sent_at")
    search_fields = ("phone_number", "message", "student__full_name", "student__admission_number")
    readonly_fields = ("student", "phone_number", "message", "log_time", "sent_at", "success", "response")
    ordering = ("-sent_at",)

    def has_add_permission(self, request):
        return False  # Prevent manual addition from admin

    def has_change_permission(self, request, obj=None):
        return False  # Make logs read-only