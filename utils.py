import datetime
import time
import requests
import os


# print(datetime.datetime.isoweekday(datetime.datetime.now()))
# print(datetime.datetime.isocalendar(datetime.datetime.now() + datetime.timedelta(days=0)).week)
#
# td = datetime.date(2023, 12, 31) - datetime.date.today()
# print(td)
# print(datetime.date(2023, 12, 31) - (datetime.date(2023, 1, 1)))
# print(datetime.datetime.isocalendar(datetime.date.today()).week)

# Измеряю скорость работы слайсеров

def check_speed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        print(f'Время выполнения: {end - start}')

    return wrapper


# def partition(l, n):
#     for i in range(0, len(l), n):
#         yield l[i:i + n]
#
#
# l = list(range(1, 9000000))
# n = 3
#
# chunks = list(partition(l, n))
# print(chunks)

# -----
# l = list(range(1, 9000000))
# n = 3
#
# chunks = [l[i:i + n] for i in range(0, len(l), n)]
# print(chunks)

# ---- Очень долго
# import itertools
#
#
# def partition(l, size):
#     for i in range(0, len(l), size):
#         yield list(itertools.islice(l, i, i + size))
#
#
# l = list(range(1, 900000))
# n = 3
#
# chunks = list(partition(l, n))
# print(chunks)

# --- быстрее 1 и 2 на 1с
# import itertools
#
#
# def partition(l, size):
#     it = iter(l)
#     return iter(lambda: tuple(itertools.islice(it, size)), ())
#
#
# l = list(range(1, 9000000))
# n = 3
#
# chunks = list(partition(l, n))
# print(chunks)

# --- Ок
# from toolz import partition
#
# l = list(range(1, 9000000))
# n = 3
#
# chunks = list(partition(n, l))
# print(chunks)

# Проверка связи с api nav by
MY_TOKEN = os.environ.get('MY_TOKEN')

NAV_URL = 'https://api.nav.by'

# response2 = requests.get(f"{NAV_URL}/info/integration.php?type=VEHICLE_LIST&token={MY_TOKEN}")
# for i in response2.json()['root']['result']['items']:
#     print(i)

# response3 = requests.get(f"{NAV_URL}/info/integration.php?type=CURRENT_POSITION&token={MY_TOKEN}&get_address=true")
# for i in response3.json()['root']['result']['items']:
#     print(i['object_id'], i['object_name'], i['place'], 'Скорость:', i['speed'])
st = datetime.datetime.now()
sts = str(st)[:-7]
fn = st - datetime.timedelta(days=5)
fns = str(fn)[:-7]
print(str(st)[:-7], str(fn)[:-7])
# узнаем пробег по GPS по каждому авто
response4 = requests.get(f"{NAV_URL}/info/integration.php?type=OBJECT_STAT_DATA&token={MY_TOKEN}&from={fns}&to={sts}")
for i in response4.json()['root']['result']['items']:
    print(round(i['distance_gps']/1000))



