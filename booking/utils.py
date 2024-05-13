import schedule
import time
import datetime
import requests
from config import settings
import threading
from .models import CarNote


def print_time():
    print(time.asctime())


def grouping_by_day(s_list):
    list_triple = []
    inner_time = None
    counter = 0
    for i in s_list:
        if not list_triple:
            list_triple.append([i])
            inner_time = i[1].date
        else:
            if i[1].date == inner_time:
                list_triple[counter].append(i)
            else:
                list_triple.append([i])
                counter += 1
                inner_time = i[1].date
    return list_triple


def request_car_day_info(db_date):
    i = 0
    # date_start = datetime.date.today() - datetime.timedelta(days=i)
    date_start = db_date
    print(f'Инфа за {date_start}')
    # date_finish = datetime.date.today() + datetime.timedelta(days=1) - datetime.timedelta(days=i)
    date_finish = db_date + datetime.timedelta(days=1)
    time_start = datetime.time(3, 0, 0)
    time_finish = datetime.time(2, 59, 59)
    response = requests.get(
        f"{settings.NAV_URL}/info/integration.php?type=OBJECT_STAT_DATA&token={settings.MY_TOKEN}&from={date_start}{' '}{time_start}&to={date_finish}{' '}{time_finish}")
    rj = response.json()['root']['result']['items']
    print('Ответ получен')
    return rj
    # for j in rj:
    #     print(j['distance_gps'] / 1000)


def request_and_insert_day_mileage():
    i = 2
    date_start = datetime.date.today() - datetime.timedelta(days=i)
    print(f'Инфа за {date_start}')
    date_finish = datetime.date.today() + datetime.timedelta(days=1) - datetime.timedelta(days=i)
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

# request_car_day_info(datetime.date.today())


# def run_threaded(func):
#     new_thread = threading.Thread(target=func)
#     new_thread.start()
#
#
# schedule.every(10).seconds.do(request_car_day_info)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
#
# print(datetime.date(2024, 4, 5))
# print(datetime.date.today())
# for day in range((datetime.date(2025, 1, 5) - datetime.date(2024, 1, 1)).days):
#     date = datetime.timedelta(days=day) + datetime.date(2024, 1, 1)
#     print(day)
