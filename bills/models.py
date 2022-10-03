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
    days_to_notify_before_expiration = models.IntegerField()
    expiration_date = models.DateField(null=True,blank=True,verbose_name='Data de vencimento')
    expiration_notification_date = models.DateField(null=True,blank=True,verbose_name='Data para notificar vencimento')
    bill_charger:BillCharger = models.ForeignKey(BillCharger,on_delete=models.CASCADE,verbose_name='Cobrador')
    bill_category:BillCategory = models.ForeignKey(BillCategory,on_delete=models.CASCADE,verbose_name='Categoria')
    status = models.CharField(choices=BILL_STATUSES,default='UNDEFINED',max_length=9)
    payment_proof_path = models.CharField(max_length=255,null=True,blank=True)
    note = models.CharField(max_length=60,blank=True,null=True,verbose_name='Nota')
    value = models.FloatField(verbose_name='Valor')

    gender = 'a'

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'