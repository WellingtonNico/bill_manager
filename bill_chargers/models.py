from django.db import models
from django.forms import ValidationError
from django.urls import reverse_lazy
from users.models import User


class BillCharger(models.Model):
    user:User = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=60,verbose_name='Nome')
    phone = models.CharField(max_length=60,blank=True,null=True,verbose_name='Telefone de contato')
    email = models.EmailField(blank=True,null=True,verbose_name='E-mail')

    gender = 'o'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cobrador'
        verbose_name_plural = 'Cobradores'
        unique_together = (('name','user'),)

    def get_absolute_url(self):
        return reverse_lazy('billcharger_update',kwargs={'pk':self.id})

    def validate_unique(self, exclude):
        querySet = BillCharger.objects.filter(user=self.user,name=self.name)
        if querySet.exists():
            if querySet.first().id != self.id:
                raise ValidationError('Já existe uma categoria com este nome')
        return super().validate_unique(exclude)