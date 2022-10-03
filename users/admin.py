from django.contrib import admin
from users.forms import UserCreateModelForm
from django.contrib.auth.admin import UserAdmin
from users.models import User


class UserModelAdmin(UserAdmin):
    list_display = ('email','first_name','is_active','is_staff','is_superuser','document')

admin.site.register(User,UserModelAdmin)
