from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Bill
from datetime import datetime,timedelta
import os


@receiver(pre_save,sender=Bill,weak=False)
def bill_pre_save_signal_handler(sender:Bill,instance:Bill,*args,**kwargs):
    if instance.status != 'PAID':
        pass




@receiver(post_save,sender=Bill,weak=False)
def bill_post_save_signal_handler(sender:Bill,instance:Bill,created,*args,**kwargs):
    pass


# @receiver(pre_delete,sender=Bill,weak=False)
# def bill_pre_delete_signal_handler(sender:Bill,instance:Bill,*args,**kwargs):
#     instance.delete_payment_proof()
