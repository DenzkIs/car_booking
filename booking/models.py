from django.contrib.auth.models import User
from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=100)

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

    def __str__(self):
        return f'{self.date} - {self.engineer} - {self.car}'

