# Generated by Django 4.2.3 on 2024-04-10 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_car_current_mileage_car_last_maintenance_mileage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carnote',
            name='km_per_day',
        ),
        migrations.AddField(
            model_name='carnote',
            name='distance_gps',
            field=models.FloatField(default=0, verbose_name='Пробег за день, км (distance_gps)'),
        ),
        migrations.AddField(
            model_name='carnote',
            name='max_speed',
            field=models.IntegerField(default=0, verbose_name='Максимальная скорость, км/ч'),
        ),
        migrations.AddField(
            model_name='carnote',
            name='run_time_seconds',
            field=models.IntegerField(default=0, verbose_name='Время езды, с (run_time)'),
        ),
        migrations.AddField(
            model_name='carnote',
            name='run_time_str',
            field=models.CharField(default=0, max_length=100, verbose_name='Время езды, ч. мин. (run_time_str)'),
        ),
        migrations.AlterField(
            model_name='car',
            name='object_id',
            field=models.IntegerField(default=0, verbose_name='object_id в системе nav.by'),
        ),
    ]
