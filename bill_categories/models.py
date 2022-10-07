from django.db import models
from django.forms import ValidationError
from django.urls import reverse_lazy
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

    def get_absolute_url(self):
        return reverse_lazy('billcategory_update',kwargs={'pk':self.id})

    def validate_unique(self, exclude):
        querySet = BillCategory.objects.filter(user=self.user,name__iexact=self.name)
        if querySet.exists():
            if querySet.first().id != self.id:
                raise ValidationError(f'Já existe uma categoria com o nome "{self.name}"')
        return super().validate_unique(exclude)