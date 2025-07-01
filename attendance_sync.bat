@echo off
cd /d D:\elburgon_attendance
call venv\Scripts\activate
echo Running at %date% %time% >> sync_log.txt
python manage.py sync_attendance >> sync_log.txt 2>&1
python manage.py send_attendance_sms >> sync_log.txt 2>&1
echo Done at %time% >> sync_log.txt
