from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import datetime
import os
import requests
from toolz import partition
from .models import Car, CarNote
from .forms import CarNoteForm, CarServiceInfoForm

MY_TOKEN = os.environ.get('MY_TOKEN')
NAV_URL = 'https://api.nav.by'


@login_required
def get_table_page(request):
    car_notes = CarNote.objects.select_related('car')
    form_list = []
    for note in car_notes:
        form = CarNoteForm(instance=note)
        if (
                request.method == 'POST'
                and str(note.id) in request.POST
                and CarNoteForm(request.POST, instance=note).is_valid()
                and request.user.is_authenticated
                and (note.engineer == '' or note.engineer == request.user.first_name)
                and (request.user.profile.access == 'sm' or request.user.profile.access == 'ad' or request.user.username == 'admin')

        ):
            form = CarNoteForm(request.POST, instance=note)
            form.save()
            note.engineer = request.user.first_name
            note.save()
        form_list.append((form, note))
    # группирую записи по 3 шт, чтобы отображать общую дату сразу на 3 машины
    form_list_three = list(partition(3, form_list))
    paginator = Paginator(form_list_three, 14)
    page_number = request.GET.get('page')
    # если первый переход на страницу - показать текущую неделю
    if page_number:
        page = paginator.get_page(page_number)
    else:
        page = paginator.get_page(round(datetime.datetime.isocalendar(datetime.date.today()).week / 2))
    day_today = datetime.date.today()
    context = {'car_notes': car_notes, 'form_list': page, 'day_today': day_today}

    return render(request, template_name='table_page.html', context=context)


def cancel_note(request, id):
    note = CarNote.objects.get(id=id)
    if note.engineer == request.user.first_name:
        note.engineer = ''
        note.city = ''
        note.comment = ''
        note.save()
    return redirect('table_page')


# нужна для генерации дней на текущий год
def create_car_notes(request):
    for day in range((datetime.date(2023, 12, 31) - datetime.date(2023, 1, 1)).days):
        date = datetime.date(2023, 1, 2) + datetime.timedelta(days=day)
        CarNote.objects.create(date=date, car=Car.objects.get(id=1))
        CarNote.objects.create(date=date, car=Car.objects.get(id=2))
        CarNote.objects.create(date=date, car=Car.objects.get(id=3))
    return redirect('table_page')


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
    nav_response = requests.get(
        f"{NAV_URL}/info/integration.php?type=CURRENT_POSITION&token={MY_TOKEN}&get_address=true")
    cars_info = nav_response.json()['root']['result']['items']
    context = {'cars_info': cars_info}
    return render(request, template_name='current_car_info.html', context=context)


def get_car_service(request):
    form = CarServiceInfoForm()
    if request.method == 'POST' and request.FILES:
        form = CarServiceInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, template_name='car_service.html', context=context)
