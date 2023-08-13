from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ACCESS_CHOICES = (
        ('sm', 'service_man'),
        ('sa', 'service_admin'),
        ('rm', 'risola_manager'),
        ('ad', 'another_driver'),
        ('fa', 'full_access'),
    )
    SHOW_WEEKS_CHOICES = (

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец')
    image = models.ImageField(default="profile_pics/default.jpg", upload_to="profile_pics", verbose_name='Фото профиля')
    access = models.CharField(max_length=2, choices=ACCESS_CHOICES, verbose_name='Уровень доступа', default='rm')

    def __str__(self):
        return f"Профиль пользователя: {self.user.username}"