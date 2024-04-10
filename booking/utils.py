import schedule
import time
import datetime
import requests
from config import settings
import threading


def print_time():
    print(time.asctime())


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
