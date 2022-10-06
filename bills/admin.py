import ast
from core.celery import app
from .models import Bill
from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from django_celery_results.models import TaskResult
from django_celery_results.admin import TaskResultAdmin



def retry_celery_task_admin_action(modeladmin, request, queryset):
    successMsg = ''
    errorMsg = ''

    for task_res in queryset.iterator():
        args = task_res.task_args
        try:
            attempts = 0
            while not type(args) in (list,tuple) and attempts < 4:
                attempts += 1
                args = ast.literal_eval(args)
            app.signature(task_res.task_name).apply_async(args=args)
            successMsg += f'{task_res.task_id} => Successfully sent to queue for retry.<br>'
        except Exception as ex:
            errorMsg += f'{task_res.task_id} => Unable to process. Error: {ex}<br>'
    messages.success(request, mark_safe(successMsg))
    messages.error(request, mark_safe(errorMsg))
retry_celery_task_admin_action.short_description = 'Retry Task'


class CustomTaskResultAdmin(TaskResultAdmin):
    actions = (retry_celery_task_admin_action,)


admin.site.unregister(TaskResult)
admin.site.register(TaskResult, CustomTaskResultAdmin)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_category','user','bill_type','status','value','created_date','expiration_date')
