from django.contrib import admin
from .models import BillCategory


@admin.register(BillCategory)
class BillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','user')
