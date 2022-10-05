import os
import glob
from datetime import datetime
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from bill_categories.models import BillCategory
from bill_chargers.models import BillCharger
from bills.constants import *
from bills.validators import *
from users.models import User


class Bill(models.Model):
    user:User = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuário')
    bill_type = models.CharField(choices=BILL_TYPES,verbose_name='Tipo',max_length=18)
    installment_total = models.IntegerField(null=True,blank=True,verbose_name='Quantidade de parcelas',validators=(only_greater_than_zero,))
    installment_sequence = models.IntegerField(null=True,blank=True,verbose_name='Número da parcela',validators=(only_greater_than_zero,))
    created_date = models.DateField(verbose_name='Data de criação')
    payment_date = models.DateField(verbose_name='Data de pagamento',null=True,blank=True,validators=(only_date_lower_or_equal_today,))
    payment_type = models.CharField(choices=BILL_PAYMENT_TYPES,verbose_name='Tipo de pagamento',max_length=18,blank=True,null=True)
    days_to_notify_before_expiration = models.IntegerField(verbose_name='Dias para notificar antes do vencimento',validators=(only_positive_numbers,))
    expiration_date = models.DateField(null=True,blank=True,verbose_name='Data de vencimento')
    expiration_notification_date = models.DateField(null=True,blank=True,verbose_name='Data para notificar vencimento')
    bill_charger:BillCharger = models.ForeignKey(BillCharger,on_delete=models.CASCADE,verbose_name='Cobrador')
    bill_category:BillCategory = models.ForeignKey(BillCategory,on_delete=models.CASCADE,verbose_name='Categoria')
    status = models.CharField(choices=BILL_STATUSES,default='UNDEFINED',max_length=9)
    note = models.CharField(max_length=60,blank=True,null=True,verbose_name='Nota')
    value = models.FloatField(verbose_name='Valor')

    # banco

    gender = 'a'

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = (('-created_date',))

    def get_absolute_url(self):
        return reverse_lazy('bill_update',kwargs={'pk':self.id})

    def get_days_to_expiration_date(self):
        if self.status in ('TO_EXPIRE','WARNING'):
            difference = (self.expiration_date - datetime.now().date()).days
            if abs(difference) == 1:
                return f'{difference} dia'
            else:
                return f'{difference} dias'
        return '-'

    def get_payment_proof_fulldir(self):
        files = glob.glob(self.user.get_payment_proofs_dir()+f'{settings.PAYMENT_PROOF_PREFIX_NAME}{self.id}.*')
        if files:
            return files[0]
        return ''

    def delete_payment_proof(self):
        fullDir = self.get_payment_proof_fulldir()
        if fullDir:
            os.remove(fullDir)