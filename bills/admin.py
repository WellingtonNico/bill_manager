from django.contrib import admin
from .models import Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_category','user','bill_type','status','value','create_date','expiration_date')
