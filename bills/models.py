import os
import glob
from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse_lazy
from bill_categories.models import BillCategory
from bill_chargers.models import BillCharger
from bills.constants import *
from bills.managers import BillManager
from bills.validators import *
from users.models import User


def get_payment_proof_path(instance,filename):
    return  f'payment_proofs/user_{instance.user.id}/payment_proof_{instance.id}.{filename.split(".")[-1]}'


def get_today_default_value():
    return datetime.now().date()


class Bill(models.Model):
    user:User = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuário')
    bill_type = models.CharField(choices=BILL_TYPES,verbose_name='Tipo',max_length=18)
    installment_total = models.IntegerField(null=True,blank=True,verbose_name='Quantidade de Parcelas',validators=(only_greater_than_zero,))
    installment_sequence = models.IntegerField(null=True,blank=True,verbose_name='Número da Parcela',validators=(only_greater_than_zero,),default=1)
    created_date = models.DateField(verbose_name='Data de Criação',default=get_today_default_value)
    payment_date = models.DateField(verbose_name='Data de Pagamento',null=True,blank=True,validators=(only_date_lower_or_equal_today,))
    payment_type = models.CharField(choices=BILL_PAYMENT_TYPES,verbose_name='Forma de Pagamento',max_length=18,blank=True,null=True)
    payment_proof_file = models.FileField(null=True,blank=True,verbose_name='Comprovante de Pagamento',upload_to=get_payment_proof_path,validators=(payment_proof_file_size_validator,payment_proof_file_format_validator))
    bank = models.CharField(choices=BILL_PAYMENT_BANKS,blank=True,null=True,verbose_name='Banco',max_length=30)
    days_to_notify_before_expiration = models.IntegerField(verbose_name='Dias para Notificar Antes do Vencimento',validators=(only_positive_numbers,),default=14)
    expiration_date = models.DateField(null=True,blank=True,verbose_name='Data de Vencimento')
    expiration_notification_date = models.DateField(null=True,blank=True,verbose_name='Data para notificar vencimento')
    bill_charger:BillCharger = models.ForeignKey(BillCharger,on_delete=models.CASCADE,verbose_name='Cobrador')
    bill_category:BillCategory = models.ForeignKey(BillCategory,on_delete=models.CASCADE,verbose_name='Categoria')
    status = models.CharField(choices=BILL_STATUSES,default='UNDEFINED',max_length=13)
    # note = models.CharField(max_length=60,blank=True,null=True,verbose_name='Comentário')
    value = models.FloatField(verbose_name='Valor')

    objects = BillManager()

    gender = 'a'

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = (('-created_date',))

    def get_absolute_url(self):
        return reverse_lazy('bill_list')

    def get_days_to_expiration_date(self):
        if self.status in ('TO_EXPIRE','WARNING','EXPIRED'):
            difference = (self.expiration_date - datetime.now().date()).days
            if abs(difference) == 1:
                return f'{difference} dia'
            else:
                return f'{difference} dias'
        return '-'

    def get_updated_status(self):
        if self.status == 'PAID':
            return self.status
        if self.expiration_date == datetime.now().date():
            return 'EXPIRES_TODAY'
        if self.expiration_date:
            if datetime.now().date() > self.expiration_date:
                return 'EXPIRED'
            if (self.expiration_date -timedelta(days=self.days_to_notify_before_expiration)) <= datetime.now().date() < self.expiration_date:
                return 'WARNING'
            else:
                return 'TO_EXPIRE'
        return 'UNDEFINED'
        

        
        
