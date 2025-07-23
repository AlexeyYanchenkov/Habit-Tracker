from celery import shared_task
import requests
from django.conf import settings

@shared_task
def send_telegram_message(chat_id, text):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url, data=payload)
    return response.json()