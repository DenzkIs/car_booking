import time
from celery import shared_task
from config.celery import app
import requests
import datetime
from django.conf import settings
from .models import CarNote
from .telegram_bot import mileage_warning


# @shared_task
# def request_car_day_info():
#     i = 2
#     date_start = datetime.date.today() - datetime.timedelta(days=i)
#     date_finish = datetime.date.today() + datetime.timedelta(days=1) - datetime.timedelta(days=i)
#     time_start = datetime.time(3, 0, 0)
#     time_finish = datetime.time(2, 59, 59)
#     response = requests.get(
#         f"{settings.NAV_URL}/info/integration.php?type=OBJECT_STAT_DATA&token={settings.MY_TOKEN}&from={date_start}{' '}{time_start}&to={date_finish}{' '}{time_finish}")
#     rj = response.json()['root']['result']['items']
#     for j in rj:
#         print(j['distance_gps'] / 1000)


@shared_task
def request_and_insert_day_mileage():
    day_ago = 1
    date_start = datetime.date.today() - datetime.timedelta(days=day_ago)
    date_finish = datetime.date.today()  # + datetime.timedelta(days=1) - datetime.timedelta(days=day_ago)
    time_start = datetime.time(3, 0, 0)
    time_finish = datetime.time(2, 59, 59)
    notes = CarNote.objects.filter(date=date_start)
    try:
        response = requests.get(
            f"{settings.NAV_URL}/info/integration.php?type=OBJECT_STAT_DATA&token={settings.MY_TOKEN}&from={date_start}{' '}{time_start}&to={date_finish}{' '}{time_finish}")
        response_json = response.json()['root']['result']['items']
        for note in notes:
            for info in response_json:
                if info.get('object_id') == str(note.car.object_id):
                    note.distance_gps = round(float(info.get('distance_gps')) / 1000, 2)
                    note.run_time_seconds = info.get('run_time')
                    note.run_time_str = info.get('run_time_str')
                    note.max_speed = info.get('max_speed')
                    note.save()
    except requests.exceptions.ConnectionError:
        print('Не удалось подключиться к серверу')


@shared_task
def add_day_mileage_to_car():
    date = datetime.date.today() - datetime.timedelta(days=1)
    notes = CarNote.objects.filter(date=date).select_related('car')
    for note in notes:
        wrote_day = note.car.mileage_included_day
        if wrote_day is None or date > wrote_day:
            current_mileage = note.car.current_mileage
            note.car.current_mileage = round(current_mileage + note.distance_gps, 2)
            note.car.mileage_included_day = date
            note.car.save()
            km_do_to = note.car.last_maintenance_mileage + note.car.maintenance_frequency - note.car.current_mileage
            if km_do_to < 2000:
                mileage_warning(note.car.brand, km_do_to)
                time.sleep(3)

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
