from django.contrib.auth.models import User
from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=100)
    object_id = models.IntegerField(default=0, db_index=True, verbose_name='object_id в системе nav.by')
    current_mileage = models.FloatField(default=0, verbose_name='Текущий пробег, км')
    last_maintenance_mileage = models.FloatField(default=0, verbose_name='Пробег при последнем ТО, км')
    maintenance_frequency = models.FloatField(default=15000, verbose_name='Частота ТО, км')


    def __str__(self):
        return self.brand


class CarNote(models.Model):
    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    engineer = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=255, null=True)
    taking_time = models.TimeField(blank=True, null=True)
    return_time = models.TimeField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    distance_gps = models.FloatField(default=0, verbose_name='Пробег за день, км (distance_gps)')
    run_time_seconds = models.IntegerField(default=0, verbose_name='Время езды, с (run_time)')
    run_time_str = models.CharField(max_length=100, default=0,verbose_name='Время езды, ч. мин. (run_time_str)')
    max_speed = models.IntegerField(default=0, verbose_name='Максимальная скорость, км/ч')

    def __str__(self):
        return f'{self.date} - {self.engineer} - {self.car}'


class CarServiceInfo(models.Model):
    title = models.CharField(max_length=255)
    report = models.FileField(upload_to='reports')

    def __str__(self):
        return self.title
