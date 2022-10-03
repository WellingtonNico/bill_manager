from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from users.validators import document_validator


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=False,unique=True)
    document = models.CharField(max_length=14,verbose_name='Documento',null=True,blank=True,validators=(document_validator,))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','username']

    def __str__(self):
        return self.first_name


