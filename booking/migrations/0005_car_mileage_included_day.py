# Generated by Django 4.2.3 on 2024-04-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_car_background_color_car_text_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='mileage_included_day',
            field=models.DateField(blank=True, null=True, verbose_name='Последний день, учтенный в текущем пробеге'),
        ),
    ]