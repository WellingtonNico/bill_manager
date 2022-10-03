from django.db import models
from bill_categories.models import BillCategory
from bill_chargers.models import BillCharger
from bills.constants import *
from users.models import User


class Bill(models.Model):
    user:User = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuário')
    bill_type = models.CharField(choices=BILL_TYPES,verbose_name='Tipo',max_length=18)
    installment_number = models.IntegerField(null=True,blank=True,verbose_name='Número da parcela')
    create_date = models.DateField(verbose_name='Data de criação')
    expiration_date = models.DateField(null=True,blank=True,verbose_name='Data de vencimento')
    expiration_notification_date = models.DateField(null=True,blank=True,verbose_name='Data para notificar vencimento')
    bill_charger:BillCharger = models.ForeignKey(BillCharger,on_delete=models.CASCADE,verbose_name='Cobrador')
    bill_category:BillCategory = models.ForeignKey(BillCategory,on_delete=models.CASCADE,verbose_name='Categoria')
    status = models.CharField(choices=BILL_STATUSES,default='UNDEFINED',max_length=9)
    value = models.FloatField(verbose_name='Valor')