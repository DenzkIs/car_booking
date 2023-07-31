from django.urls import path
from .views import get_table_page, create_car_notes

urlpatterns = [
    path('', get_table_page, name='table_page'),
    path('create/', create_car_notes, name='create_car_notes'),

]
