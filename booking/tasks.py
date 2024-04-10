import time
from celery import shared_task
from config.celery import app
import requests
import datetime
from django.conf import settings


@shared_task
def request_car_day_info():
    i = 0
    date_start = datetime.date.today() - datetime.timedelta(days=i)
    print(f'Инфа за {date_start}')
    date_finish = datetime.date.today() + datetime.timedelta(days=1) - datetime.timedelta(days=i)
    time_start = datetime.time(3, 0, 0)
    time_finish = datetime.time(2, 59, 59)
    response = requests.get(
        f"{settings.NAV_URL}/info/integration.php?type=OBJECT_STAT_DATA&token={settings.MY_TOKEN}&from={date_start}{' '}{time_start}&to={date_finish}{' '}{time_finish}")
    rj = response.json()['root']['result']['items']
    for j in rj:
        print(j['distance_gps'] / 1000)

#
# @shared_task
# def print_hello():
#     with open('files_cel/hello.txt', 'a+') as f:
#         f.write(f'\n{time.asctime()}\n')
#     for i in range(1, 6):
#         time.sleep(3)
#         text = f'{i})---Hello---\n'
#         print(text)
#         with open('files_cel/hello.txt', 'a+') as f:
#             f.write(text)
#
#     return 'Все кончено!'
#
#
# @app.task
# def print_time():
#     print(f'------------ Текущее время: {time.asctime()} ------------')
#     return 'Успешно'
