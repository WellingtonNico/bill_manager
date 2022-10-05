import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from users.validators import document_validator
from django.conf import settings
from pathlib import Path


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=False,unique=True)
    document = models.CharField(max_length=14,verbose_name='Documento',null=True,blank=True,validators=(document_validator,))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','username']

    def __str__(self):
        return self.first_name

    def get_bills(self):
        return self.bill_set.all()

    def get_billcategories(self):
        return self.billcategory_set.all()

    def get_billchargers(self):
        return self.billcharger_set.all()

    def get_payment_proofs_dir(self):
        fullDir = settings.PAYMENT_PROOFS_DIR+f'/user_{self.id}/'
        if not os.path.exists(fullDir):
            path = Path(fullDir)
            path.mkdir(parents=True,exist_ok=True)
        return fullDir



