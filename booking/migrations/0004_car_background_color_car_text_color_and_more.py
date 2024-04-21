# Generated by Django 4.2.3 on 2024-04-21 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_remove_carnote_km_per_day_carnote_distance_gps_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='background_color',
            field=models.CharField(default='white', max_length=100),
        ),
        migrations.AddField(
            model_name='car',
            name='text_color',
            field=models.CharField(default='black', max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='object_id',
            field=models.IntegerField(db_index=True, default=0, verbose_name='object_id в системе nav.by'),
        ),
    ]
