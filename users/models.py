import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from users.validators import document_validator
from django.conf import settings
from pathlib import Path
import shutil


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
        fullDir = self.get_full_payment_proofs_dir()
        if not os.path.exists(fullDir):
            path = Path(fullDir)
            path.mkdir(parents=True,exist_ok=True)
        return fullDir

    def has_billrelatory(self):
        try:
            return self.billrelatory
        except:
            return False

    def delete_payment_proofs_folder(self):
        shutil.rmtree(self.get_full_payment_proofs_dir())




