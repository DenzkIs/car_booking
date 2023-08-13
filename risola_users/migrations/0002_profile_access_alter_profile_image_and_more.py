# Generated by Django 4.2.3 on 2023-08-13 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('risola_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='access',
            field=models.CharField(choices=[('sm', 'service_man'), ('sa', 'service_admin'), ('rm', 'risola_manager'), ('ad', 'another_driver'), ('fa', 'full_access')], default='rm', max_length=2, verbose_name='Уровень доступа'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics', verbose_name='Фото профиля'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]
