from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    f_requests = models.ManyToManyField('self', blank=True, symmetrical=False)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
