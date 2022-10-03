from django.db import models
from users.models import User


class BillCharger(models.Model):
    user:User = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=60,verbose_name='Nome')
    phone = models.CharField(max_length=60,blank=True,null=True,verbose_name='Telefone de contato')
    email = models.EmailField(blank=True,null=True,verbose_name='E-mail')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cobrador'
        verbose_name_plural = 'Cobradores'
        unique_together = (('name','user'),)