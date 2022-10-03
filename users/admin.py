from django.contrib import admin

from users.models import User


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('first_name','email','document')

admin.site.register(User,UserModelAdmin)
