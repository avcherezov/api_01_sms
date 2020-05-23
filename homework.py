import time

import requests
from twilio.rest import Client

import os
from dotenv import load_dotenv 
load_dotenv()


account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')

url = 'https://api.vk.com/method/users.get'


def get_status(user_id):
    params = {
        'access_token':os.getenv('access_token'),
        'user_ids':user_id,
        'fields':'online',
        'name_case':'Nom',
        'v': '5.92', 
    }
    user_status = requests.post(url, params=params).json()['response'][0]['online']
    return user_status  # Верните статус пользователя в ВК


def sms_sender(sms_text):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
            body=f"{sms_text}",
            from_=NUMBER_FROM,
            to=NUMBER_TO
        )
    return message.sid  # Верните sid отправленного сообщения из Twilio


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
