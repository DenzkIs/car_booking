from django.urls import path
from .views import get_table_page, create_car_notes, cancel_note

urlpatterns = [
    path('', get_table_page, name='table_page'),
    path('create/', create_car_notes, name='create_car_notes'),
    path('cancel_note/<int:id>/', cancel_note, name='cancel_note'),

]
