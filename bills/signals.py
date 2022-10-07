from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from .models import Bill
from datetime import timedelta


@receiver(pre_save,sender=Bill,weak=False)
def bill_pre_save_signal_handler(sender:Bill,instance:Bill,*args,**kwargs):
    instance.status = instance.get_updated_status()
    if instance.status in ('EXPIRED','EXPIRES_TODAY','TO_EXPIRE','WARNING') and instance.expiration_date:
        instance.expiration_notification_date = instance.expiration_date - timedelta(days=instance.days_to_notify_before_expiration)


@receiver(post_save,sender=Bill,weak=False)
def bill_post_save_signal_handler(sender:Bill,instance:Bill,created,*args,**kwargs):
    if created and instance.bill_type == 'INSTALLED':
        installmentBills = []
        for n in range(instance.installment_sequence,instance.installment_total):
            installmentBill = Bill(
                user=instance.user,
                bill_charger=instance.bill_charger,
                bill_category=instance.bill_category,
                installment_sequence=n+1,
                **model_to_dict(
                    instance,exclude=(
                        'id','bill_category','bill_charger','user',
                        'installment_sequence',
                    )
                )
            )
            newExpirationDate = installmentBill.expiration_date + timedelta(days=30 * n)
            if newExpirationDate.month == installmentBill.expiration_date.month:
                newExpirationDate += timedelta(days=2)
            newExpirationDate = newExpirationDate.replace(day=instance.expiration_date.day)
            installmentBill.expiration_date = newExpirationDate
            installmentBill.expiration_notification_date = installmentBill.expiration_date - timedelta(days=instance.days_to_notify_before_expiration)
            installmentBill.status = installmentBill.get_updated_status()
            installmentBills.append(installmentBill)
        Bill.objects.bulk_create(installmentBills)



# @receiver(pre_delete,sender=Bill,weak=False)
# def bill_pre_delete_signal_handler(sender:Bill,instance:Bill,*args,**kwargs):
#     instance.delete_payment_proof()
