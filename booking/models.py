from django.contrib.auth.models import User
from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=100)
    object_id = models.IntegerField(default=0, verbose_name='Object_id в системе nav.by')

    def __str__(self):
        return self.brand


class CarNote(models.Model):
    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    engineer = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, null=True)
    taking_time = models.TimeField(blank=True, null=True)
    return_time = models.TimeField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    km_per_day = models.IntegerField(default=0, verbose_name='Пробег за день (км)')

    def __str__(self):
        return f'{self.date} - {self.engineer} - {self.car}'


class CarServiceInfo(models.Model):
    title = models.CharField(max_length=255)
    report = models.FileField(upload_to='reports')

    def __str__(self):
        return self.title
