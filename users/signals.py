from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver
from .models import User


@receiver(pre_save,sender=User,weak=False)
def userPreSaveSignalHandler(sender:User,instance:User,*args,**kwargs):
    instance.username = instance.email
