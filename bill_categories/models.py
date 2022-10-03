from django.db import models
from users.models import User

class BillCategory(models.Model):
    user:User = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=60,verbose_name='Nome')

    def __str__(self):
        return self.name
