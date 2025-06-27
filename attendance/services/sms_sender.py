import requests
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

def send_sms(phone_number, message):
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
        response.raise_for_status()

        data = response.json()
        print(f"SMS response: {data}")

        return data.get("ErrorCode") == "0" or response.status_code == 200

    except requests.RequestException as e:
        print(f"Failed to send SMS to {phone_number}: {e}")
        return False
