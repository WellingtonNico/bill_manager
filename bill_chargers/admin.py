from django.contrib import admin
from .models import BillCharger


@admin.register(BillCharger)
class BillChargerAdmin(admin.ModelAdmin):
    list_display = ('name','user')