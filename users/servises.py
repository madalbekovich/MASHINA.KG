from .models import Users
from django.conf import settings
from django.utils import timezone
import requests


def send_sms(phone, message, code):
    user = Users.objects.get(phone=phone)
    new_phone = "".join(filter(str.isdigit, phone))
    xml_data = f"""<?xml version="1.0" encoding="UTF-8"?><message><login>nurbеktmusic</login><pwd>Nuh020207</pwd><sender>SMSPRO.KG</sender><text>{message} {code}</text><phones><phone>996501774428</phone></phones></message>"""

    # xml_data = f"""<?xml version="1.0" encoding="UTF-8"?><message><login>into</login><pwd>YqsdM_ir</pwd><sender>SMSPRO.KG</sender><text>{new_phone} {code}</text><phones><phone>996707402858</phone></phones></message>"""
    headers = {"Content-Type": "application/xml"}

    url = "https://smspro.nikita.kg/api/message"

    response = requests.post(url, data=xml_data.encode("utf-8"), headers=headers)

    # Обновляем время последней отправки кода

    if response.status_code == 200:
        user.last_code_sent_at = timezone.now()
        user.save()
        return True
    return False


def os_getbalance(user_id):
    url = settings.ONE_C_BAL

    params = {"user_id": user_id}

    headers = {"Authorization": settings.ONE_C}
    response = requests.get(url, params=params, headers=headers)

    # print(f"\n\n1С says\n{response.text}\n\n")

    if response.status_code == 200:
        balance_data = response.json()
        balance = balance_data["balance"]
        return f"{balance}"
    else:
        print("Не удалось получить баланс. Код состояния:", response.status_code)
