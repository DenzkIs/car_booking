from django.contrib import admin
from .models import Car, CarNote, CarServiceInfo

admin.site.register(Car)
admin.site.register(CarNote)
admin.site.register(CarServiceInfo)
