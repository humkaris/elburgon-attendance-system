import requests
from attendance.models import SMSLog
def normalize_phone_number(number):
    number = number.strip().replace(" ", "")
    if number.startswith("0") and len(number) == 10:
        return "254" + number[1:]
    elif number.startswith("+"):
        return number[1:]  # remove leading "+"
    elif number.startswith("254") and len(number) == 12:
        return number
    else:
        # fallback, return original
        return number

def send_sms(phone_number, message, student=None, log_time=None):
    
    base_url = "http://smsportal.hostpinnacle.co.ke/SMSApi/send"
    params = {
        "userid": "Breccia",
        "password": "Mjomba2020",
        "sendMethod": "quick",
        "senderid": "BrecciaTech",
        "msgType": "text",
        "duplicatecheck": "true",
        "output": "json",
        "mobile": normalize_phone_number(phone_number),
        "msg": message
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        success = data.get("ErrorCode") == "0" or response.status_code == 200

        # Save log
        SMSLog.objects.create(
            student=student,
            phone_number=phone_number,
            message=message,
            success=success,
            response=data
        )

        print(f"SMS response: {data}")
        return success

    except requests.RequestException as e:
        # Save failed log
        SMSLog.objects.create(
            student=student,
            phone_number=phone_number,
            message=message,
            log_time=log_time,
            success=False,
            response={"error": str(e)}
        )

        print(f"Failed to send SMS to {phone_number}: {e}")
        return False