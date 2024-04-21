from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    class WeeksChoices(models.IntegerChoices):
        ONE_WEEK = 1
        TWO_WEEKS = 2

    ACCESS_CHOICES = (
        ('sm', 'service_man'),
        ('sa', 'service_admin'),
        ('rm', 'risola_manager'),
        ('ad', 'another_driver'),
        ('fa', 'full_access'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец')
    image = models.ImageField(default="profile_pics/default.jpg", upload_to="profile_pics", verbose_name='Фото профиля')
    access = models.CharField(max_length=2, choices=ACCESS_CHOICES, verbose_name='Уровень доступа', default='rm')
    show_weeks = models.IntegerField(choices=WeeksChoices.choices, verbose_name='Отображать недель',
                                     default=WeeksChoices.ONE_WEEK)
    text_color = models.CharField(max_length=100, default='black')
    background_color = models.CharField(max_length=100, default='white')

    def save(self, **kwargs):
        super().save(**kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            print(self.image.path)

    def __str__(self):
        return f"Профиль пользователя: {self.user.username}"
