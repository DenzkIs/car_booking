from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import datetime
from .models import Car, CarNote
from .forms import CarNoteForm


def get_table_page(request):
    HttpResponseRedirect('/?page=7')
    car_notes = CarNote.objects.select_related('car')
    form_list = []
    for note in car_notes:
        form = CarNoteForm(instance=note)
        if request.method == 'POST' and str(note.id) in request.POST:
            form = CarNoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                note.engineer = request.user.first_name
                print(note.engineer)
                note.save()
        form_list.append((form, note))
    paginator = Paginator(form_list, 21)
    page_number = request.GET.get('page')
    # если первый переход на страницу - показать текущую неделю
    if page_number:
        page = paginator.get_page(page_number)
    else:
        page = paginator.get_page(datetime.datetime.isocalendar(datetime.date.today()).week)
    print(page_number)
    context = {'car_notes': car_notes, 'form_list': page}

    return render(request, template_name='table_page.html', context=context)


def create_car_notes(request):
    for day in range((datetime.date(2023, 12, 31) - datetime.date(2023, 1, 1)).days):
        date = datetime.date(2023, 1, 2) + datetime.timedelta(days=day)
        CarNote.objects.create(date=date, car=Car.objects.get(id=1))
        CarNote.objects.create(date=date, car=Car.objects.get(id=2))
        CarNote.objects.create(date=date, car=Car.objects.get(id=3))
    return redirect('table_page')

# <h2><a href="{% url 'create_car_notes' %}">Заполнить таблицу</a></h2>
