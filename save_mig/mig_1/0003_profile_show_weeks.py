# Generated by Django 4.2.3 on 2023-08-13 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risola_users', '0002_profile_access_alter_profile_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='show_weeks',
            field=models.IntegerField(choices=[(1, 'One Week'), (2, 'Two Weeks')], default=1, verbose_name='Отображать недель'),
        ),
    ]