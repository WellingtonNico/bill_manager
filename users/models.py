from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=False,unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','username']
