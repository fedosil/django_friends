from django.db import models
from django.contrib.auth.models import AbstractUser

FRIENDS = 'Friends'
FOLLOWER = 'Follower'
SUBSCRIPTION = 'Subscription'
NO_STATUS = 'No status'


class User(AbstractUser):
    f_requests = models.ManyToManyField('self', blank=True, symmetrical=False)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} | id: {self.pk}'

    def get_friends(self):
        return self.friends.all()

    def get_requests(self):
        return self.f_requests.all()

    def get_followers(self):
        return User.objects.filter(f_requests=self.pk)

    def status(self, user_id):
        obj = User.objects.get(pk=user_id)
        if obj in self.get_friends():
            return FRIENDS
        elif obj in self.get_requests():
            return SUBSCRIPTION
        elif obj in self.get_followers():
            return FOLLOWER
        return NO_STATUS

    def follow(self, user_id):
        obj = User.objects.get(pk=user_id)
        if self.status(user_id) == FRIENDS:
            return FRIENDS
        elif self.status(user_id) == FOLLOWER:
            obj.f_requests.remove(self.id)
            self.friends.add(user_id)
            return FRIENDS
        elif self.status(user_id) == SUBSCRIPTION:
            return SUBSCRIPTION
        elif self.status(user_id) == NO_STATUS:
            self.f_requests.add(user_id)
            return SUBSCRIPTION


