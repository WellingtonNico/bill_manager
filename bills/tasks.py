from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Bill
from datetime import datetime,timedelta


@shared_task(name='process_user_bills',auto_retry_for=(Exception,))
def process_user_bills(userId):
    ''' 
    responsável por fazer o processamento de todas as contas do usuário
    que precisem ser atualizadas no dia em que a task rodar
    '''
    # primeiro ajustase DEVE filtrar por status específicos
    statusesToSearch = ('EXPIRED','TO_EXPIRE','WARNING','EXPIRES_TODAY')
    expiresTodayBills = Bill.objects.filter(
        user__id=userId,expiration_date=datetime.now().date(),
        status__in=statusesToSearch
    ).update(status='EXPIRES_TODAY')
    notifyTodayBills = Bill.objects.filter(
        user__id=userId,expiration_notification_date=datetime.now().date(),
        status__in=statusesToSearch
    ).update(status='WARNING')
    expiredBills = Bill.objects.filter(
        user__id=userId,expiration_notification_date=datetime.now().date() - timedelta(days=1),
        status__in=statusesToSearch
    ).update(status='EXPIRED')

    user = get_user_model.objects.get(id=userId)
    expiresTodayBills.update(status='EXPIRES_TODAY')
