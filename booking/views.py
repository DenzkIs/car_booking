from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
import datetime
import os
import requests
from toolz import partition
from .telegram_bot import say_in_chat, mileage_warning
from .models import Car, CarNote
from .forms import CarNoteForm, CarServiceInfoForm, ChooseTimeRange
from dotenv import dotenv_values
# from . import utils
import time
from .utils import request_car_day_info, grouping_by_day
import csv

User = get_user_model()

# MY_TOKEN = os.environ.get('MY_TOKEN')
NAV_URL = 'https://api.nav.by'
env_keys = dotenv_values()
MY_TOKEN = env_keys.get('MY_TOKEN')


@login_required
def get_table_page(request):
    # print(time.asctime())
    car_notes = CarNote.objects.select_related('car').order_by('date')
    form_list = []
    for note in car_notes:
        form = CarNoteForm(instance=note)
        if (
                request.method == 'POST'
                and str(note.id) in request.POST
                and CarNoteForm(request.POST, instance=note).is_valid()
                and request.user.is_authenticated
                and (note.engineer == '' or note.engineer == request.user.first_name)
                and (
                request.user.profile.access == 'sm' or request.user.profile.access == 'ad' or request.user.username == 'admin')

        ):
            form = CarNoteForm(request.POST, instance=note)
            form.save()
            note.engineer = request.user.first_name
            note.save()
            say_in_chat(note)
        form_list.append((form, note))
    # группирую записи по 3 шт, чтобы отображать общую дату сразу на 3 машины
    # form_list_three = list(partition(3, form_list))  # чуть быстрее, но в случае удаления машины, полетит верстка
    form_list_three = grouping_by_day(form_list)
    paginator = Paginator(form_list_three, 7)
    page_number = request.GET.get('page')
    # если первый переход на страницу - показать текущую неделю
    if page_number:
        page = paginator.get_page(page_number)
    else:
        page = paginator.get_page(datetime.datetime.isocalendar(datetime.date.today()).week)
    day_today = datetime.date.today()
    context = {'car_notes': car_notes, 'form_list': page, 'day_today': day_today}
    return render(request, template_name='table_page.html', context=context)


@login_required
def get_two_tables_page(request):
    today = datetime.date.today()
    weekday = datetime.datetime.isocalendar(today).weekday
    # print(today, 'число сегодня')
    # print(datetime.datetime.isocalendar(datetime.date.today()).week, 'текущая неделя')
    # print(weekday, 'день недели')
    # 6 недель
    start_day = today - datetime.timedelta(days=weekday + 13)
    # print(start_day, 'начало отсчета')
    end_day = start_day + datetime.timedelta(days=41)
    # print(end_day, 'конец отсчета')

    car_notes = CarNote.objects.select_related('car').filter(date__range=(start_day, end_day)).order_by('date',
                                                                                                        'car__brand')

    form_list = []
    for note in car_notes:
        form = CarNoteForm(instance=note)
        if (
                request.method == 'POST'
                and str(note.id) in request.POST
                and CarNoteForm(request.POST, instance=note).is_valid()
                and request.user.is_authenticated
                and (note.engineer == '' or note.engineer == request.user.first_name)
                and (
                request.user.profile.access == 'sm' or request.user.profile.access == 'ad' or request.user.username == 'admin')

        ):
            form = CarNoteForm(request.POST, instance=note)
            form.save()
            note.engineer = request.user.first_name
            note.save()
            say_in_chat(note)
        form_list.append((form, note))
    # группирую записи по 3 шт, чтобы отображать общую дату сразу на 3 машины
    # form_list_three = list(partition(3, form_list))  # чуть быстрее, но в случае удаления машины, полетит верстка
    form_list_three = grouping_by_day(form_list)
    paginator = Paginator(form_list_three, 14)
    page_number = request.GET.get('page')
    # если первый переход на страницу - показать текущую неделю
    if page_number:
        page = paginator.get_page(page_number)
    else:
        page = paginator.get_page(2)
    day_today = datetime.date.today()
    context = {'car_notes': car_notes, 'form_list': page, 'form_list_first': page[:7], 'form_list_second': page[7:],
               'day_today': day_today}
    return render(request, template_name='base_template2.html', context=context)


def get_grid_page(request):
    car_notes = CarNote.objects.select_related('car').order_by('date', 'car__brand')
    form_list = []
    for note in car_notes:
        form = CarNoteForm(instance=note)
        if (
                request.method == 'POST'
                and str(note.id) in request.POST
                and CarNoteForm(request.POST, instance=note).is_valid()
                and request.user.is_authenticated
                and (note.engineer == '' or note.engineer == request.user.first_name)
                and (
                request.user.profile.access == 'sm' or request.user.profile.access == 'ad' or request.user.username == 'admin')

        ):
            form = CarNoteForm(request.POST, instance=note)
            form.save()
            note.engineer = request.user.first_name
            note.save()
            say_in_chat(note)
        form_list.append((form, note))
    # группирую записи по 3 шт, чтобы отображать общую дату сразу на 3 машины
    # form_list_three = list(partition(3, form_list))  # чуть быстрее, но в случае удаления машины, полетит верстка
    form_list_three = grouping_by_day(form_list)
    paginator = Paginator(form_list_three, 7)
    page_number = request.GET.get('page')
    # если первый переход на страницу - показать текущую неделю
    if page_number:
        page = paginator.get_page(page_number)
    else:
        page = paginator.get_page(datetime.datetime.isocalendar(datetime.date.today()).week)
    day_today = datetime.date.today()
    context = {'car_notes': car_notes, 'form_list': page, 'day_today': day_today}
    return render(request, template_name='base_template.html', context=context)


def cancel_note(request, id):
    note = CarNote.objects.get(id=id)
    if note.engineer == request.user.first_name:
        say_in_chat(note, 'Отмена записи:')
        note.engineer = ''
        note.city = ''
        note.comment = ''
        note.save()
    return redirect('table_page')


# нужна для генерации дней на текущий год
def create_car_notes(request):
    for day in range((datetime.date(2025, 1, 6) - datetime.date(2024, 1, 1)).days):
        date = datetime.timedelta(days=day) + datetime.date(2024, 1, 1)
        CarNote.objects.create(date=date, car=Car.objects.get(id=1))
        CarNote.objects.create(date=date, car=Car.objects.get(id=2))
        CarNote.objects.create(date=date, car=Car.objects.get(id=3))
    return redirect('table_page')


def delete_all_car_notes(request):
    CarNote.objects.all()  # .delete()
    return HttpResponse('Все записи удалены')


# <h2><a href="{% url 'create_car_notes' %}">Заполнить таблицу</a></h2>
# тестовая таблица (будет удалена)
def table_with_rowspan(request):
    notes = list(partition(3, CarNote.objects.select_related('car')))
    context = {'notes': notes}
    # for n in notes:
    #     for i in n:
    #         print(i.date, i.car, i.engineer)
    return render(request, template_name='table_with_rowspan.html', context=context)


def get_current_car_info(request):
    try:
        nav_response = requests.get(
            f"{NAV_URL}/info/integration.php?type=CURRENT_POSITION&token={MY_TOKEN}&get_address=true")
        cars_info = nav_response.json()['root']['result']['items']
        context = {'cars_info': cars_info}
        # for note in CarNote.objects.all().order_by('date').filter(date__gte=datetime.date(2024, 4, 11)):
        #     print(note.date)
        return render(request, template_name='current_car_info.html', context=context)
    except requests.exceptions.ConnectionError:
        print('Ошибка подключения к серверу')
        return redirect('two_tables_page')


def get_car_service(request):
    form = CarServiceInfoForm()
    if request.method == 'POST' and request.FILES:
        form = CarServiceInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, template_name='car_service.html', context=context)


def get_car_day_info(request):
    date = datetime.date(2024, 4, 5)
    time_start = datetime.time(0, 0, 0)
    time_finish = datetime.time(23, 59, 59)
    response = requests.get(
        f"{NAV_URL}/info/integration.php?type=OBJECT_STAT_DATA&token={MY_TOKEN}&from={date}{' '}{time_start}&to={date}{' '}{time_finish}")
    rj = response.json()['root']['result']['items']
    print(rj)
    nav_info = sorted(rj, key=lambda c: c['object_id'])[1:]
    cars = CarNote.objects.filter(date=date)
    bd_info = sorted(cars, key=lambda c: c.car.object_id)
    for nav, bd in zip(nav_info, bd_info):
        bd.km_per_day = round(nav['distance_gps'] / 1000)
        bd.save()
        print(bd.km_per_day, bd.car)

    return render(request, template_name='car_day_info.html')


def insert_car_info(request):
    """
    Заполняет базу данных с начала записей до текущей даты
    :param request:
    :return None:
    """
    processed_date = None
    day_nav_info = None
    notes = CarNote.objects.all().order_by('date')  # .filter(date__gte=datetime.date(2024, 4, 11))
    # notes_2 = []
    # for n in notes:
    #     if n.date == datetime.date.today():
    #         notes_2.append(n)
    for note in notes:
        if note.date > datetime.date.today():
            break
        if note.date == processed_date:
            for info in day_nav_info:
                if info.get('object_id') == str(note.car.object_id):
                    note.distance_gps = round(float(info.get('distance_gps')) / 1000, 2)
                    note.run_time_seconds = info.get('run_time')
                    note.run_time_str = info.get('run_time_str')
                    note.max_speed = info.get('max_speed')
                    note.save()
        else:
            processed_date = note.date
            day_nav_info = request_car_day_info(processed_date)
            print('запрос сделан')
            for info in day_nav_info:
                if info.get('object_id') == str(note.car.object_id):
                    note.distance_gps = round(float(info.get('distance_gps')) / 1000, 2)
                    note.run_time_seconds = info.get('run_time')
                    note.run_time_str = info.get('run_time_str')
                    note.max_speed = info.get('max_speed')
                    note.save()
            time.sleep(1)
        print(note.date, '------', note.distance_gps)

    print('База заполнена')
    return HttpResponse(f'{datetime.datetime.now()} - выполнено')


def insert_from_csv(request):
    notes = CarNote.objects.filter(car__brand='Джили').order_by('date')
    with open('D:\Downloads_chrome\Geely.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        for row in reader:
            date_string = row[0]
            city = row[2]
            engineer = row[3]
            day, month, year = date_string.split('.')
            normal_date = datetime.date(day=int(day), month=int(month), year=int(year))
            for note in notes:
                if note.date == normal_date:
                    note.city = city.capitalize()
                    if engineer.capitalize() == 'Выбор':
                        engineer = ''
                    note.engineer = engineer.capitalize()
                    note.save()
                    print(note)
                    continue
        print('База заполнена')

    return HttpResponse('готово')


def get_statistic(request):
    if request.method == "POST":
        form = ChooseTimeRange(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('start')
            finish = form.cleaned_data.get('finish')
            denis = CarNote.objects.filter(engineer='Денис')
            kostya = CarNote.objects.filter(engineer='Костя')
            andrei = CarNote.objects.filter(engineer='Андрей')
            misha = CarNote.objects.filter(engineer='Миша')
            km_denis, km_kostya, km_andrei, km_misha = 0, 0, 0, 0
            for note in denis:
                km_denis += note.distance_gps
            for note in kostya:
                km_kostya += note.distance_gps
            for note in andrei:
                km_andrei += note.distance_gps
            for note in misha:
                km_misha += note.distance_gps
            context = {'form': form, 'km_denis': km_denis, 'km_kostya': km_kostya, 'km_andrei': km_andrei, 'km_misha': km_misha}
            return render(request, template_name='statistic.html', context=context)
    else:
        form = ChooseTimeRange()
    context = {'form': form}
    return render(request, template_name='statistic.html', context=context)


def get_base_template(request):
    return render(request, template_name='base_template.html')


# =============================================
def grid_table(request):
    start = time.time()
    notes = CarNote.objects.all().select_related('car').order_by('date')
    group_notes = grouping_by_day(notes)
    print(time.time() - start)
    context = {'group_notes': group_notes}
    return render(request, template_name='base_template.html', context=context)


def test_celery_daily_task(request):
    i = 2
    date_start = datetime.date.today() - datetime.timedelta(days=i)
    print(f'Инфа за {date_start}')
    date_finish = datetime.date.today() + datetime.timedelta(days=1) - datetime.timedelta(days=i)
    time_start = datetime.time(3, 0, 0)
    time_finish = datetime.time(2, 59, 59)
    notes = CarNote.objects.filter(date=date_start)
    try:
        response = requests.get(
            f"{NAV_URL}/info/integration.php?type=OBJECT_STAT_DATA&token={MY_TOKEN}&from={date_start}{' '}{time_start}&to={date_finish}{' '}{time_finish}")
        response_json = response.json()['root']['result']['items']
        for note in notes:
            for info in response_json:
                if info.get('object_id') == str(note.car.object_id):
                    note.distance_gps = round(float(info.get('distance_gps')) / 1000, 2)
                    note.run_time_seconds = info.get('run_time')
                    note.run_time_str = info.get('run_time_str')
                    note.max_speed = info.get('max_speed')
                    note.save()
                    print(note.distance_gps)
    except requests.exceptions.ConnectionError:
        print('Не удалось подключиться к серверу')
    return HttpResponse('Все ок')


def test_refresh_mileage(request):
    date = datetime.date.today() - datetime.timedelta(days=3)
    notes = CarNote.objects.filter(date=date).select_related('car')
    for note in notes:
        wrote_day = note.car.mileage_included_day
        if wrote_day is None or True:  # date > wrote_day:
            current_mileage = note.car.current_mileage
            note.car.current_mileage = round(current_mileage + note.distance_gps, 2)
            note.car.mileage_included_day = date
            note.car.save()
            km_do_to = note.car.last_maintenance_mileage + note.car.maintenance_frequency - note.car.current_mileage
            if km_do_to < 2000:
                print(f'До следующего TO {note.car.brand} осталось {km_do_to} км !!!')
                mileage_warning(note.car.brand, km_do_to)
                time.sleep(3)
    print([note.car.current_mileage for note in notes])
    return HttpResponse('Все ок')
