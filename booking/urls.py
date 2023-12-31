from django.urls import path
from .views import (get_table_page,
                    create_car_notes,
                    cancel_note,
                    table_with_rowspan,
                    get_current_car_info,
                    get_car_service,
                    get_car_day_info,
                    delete_all_car_notes,
                    )

urlpatterns = [
    path('', get_table_page, name='table_page'),
    path('create/', create_car_notes, name='create_car_notes'),
    path('delete/', delete_all_car_notes, name='delete_all_car_notes'),
    path('cancel_note/<int:id>/', cancel_note, name='cancel_note'),
    path('table_with_rowspan/', table_with_rowspan, name='table_with_rowspan'),
    path('current_car_info/', get_current_car_info, name='current_car_info'),
    path('car_service/', get_car_service, name='car_service'),
    path('car_day_info/', get_car_day_info, name='car_day_info'),


]
