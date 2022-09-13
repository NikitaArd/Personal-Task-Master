from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=35, blank=False, verbose_name='User name')
    email = models.EmailField(unique=True, blank=False, verbose_name='User e-mail')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Task(models.Model):
    title = models.CharField(max_length=300, blank=False, verbose_name='Task title')
    doneStatus = models.BooleanField(default=False, verbose_name='Done ?')
    date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Time and Data')
    byUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='By')

    objects = None

    def __str__(self):
        # For better orientation between entries in the admin panel
        return '{} - {}'.format(self.title, self.byUser)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-date']



