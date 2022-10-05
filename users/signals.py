from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver
from .models import User


@receiver(pre_save,sender=User,weak=False)
def userPreSaveSignalHandler(sender:User,instance:User,*args,**kwargs):
    instance.username = instance.email

@receiver(pre_delete,sender=User,weak=False)
def userPreDeleteSignalHandler(sender:User,instance:User,*args,**kwargs):
    instance.delete_payment_proofs_folder()