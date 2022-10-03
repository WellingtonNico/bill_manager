from django.db import models
from users.models import User

class BillCategory(models.Model):
    user:User = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=60,verbose_name='Nome')

    gender = 'a'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = (('name','user'),)
