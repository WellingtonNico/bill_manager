from celery import shared_task
from django.contrib.auth import get_user_model
from core.tasks import send_mail_task
from .models import Bill
from datetime import datetime,timedelta


def build_email_relatory(userId):
    user = get_user_model().objects.get(id=userId)

    statusesToSearch = ('EXPIRED','TO_EXPIRE','WARNING','EXPIRES_TODAY')
    notifyTodayBills = Bill.objects.filter(
        user__id=userId,expiration_notification_date=datetime.now().date(),
        days_to_notify_before_expiration__gt=0,
        status__in=statusesToSearch
    ).update(status='WARNING')
    expiresTodayBills = Bill.objects.filter(
        user__id=userId,expiration_date=datetime.now().date(),
        status__in=statusesToSearch
    ).update(status='EXPIRES_TODAY')
    expiredBills = Bill.objects.filter(
        user__id=userId,expiration_date=datetime.now().date() - timedelta(days=1),
        status__in=statusesToSearch
    ).update(status='EXPIRED')
    totalOnWarning = Bill.objects.filter(
        user_id=userId,status='WARNING'
    ).count()

    emailContent = f'''

Olá {user.first_name}!

Segue abaixo o seu relatório diário de contas:
'''

    messagePrefix = lambda x:f"\n * Você tem {x} {'contas' if x > 1 else 'conta'} que"

    if not any((expiresTodayBills,expiredBills,notifyTodayBills,totalOnWarning)):
        return
    if expiresTodayBills:
        emailContent += f"{messagePrefix(expiresTodayBills)} {'vencem' if expiresTodayBills > 1 else 'vence'} hoje\n"
    
    if expiredBills:
        emailContent += f"{messagePrefix(expiredBills)} {'venceram' if expiredBills > 1 else 'venceu'} ontem\n"

    if notifyTodayBills:
        emailContent += f"{messagePrefix(notifyTodayBills)} {'entraram' if notifyTodayBills > 1 else 'entrou'} em estatus de ATENÇÃO hoje\n"

    if notifyTodayBills:
        emailContent += f"{messagePrefix(notifyTodayBills)} {'estão' if notifyTodayBills > 1 else 'está'} em estatus de ATENÇÃO\n"

    return emailContent

@shared_task(name='process_user_bills',auto_retry_for=(Exception,),max_retries=5)
def process_user_bills(userId):
    ''' 
    responsável por fazer o processamento de todas as contas do usuário
    que precisem ser atualizadas no dia em que a task rodar
    '''
    # primeiro ajustase DEVE filtrar por status específicos
    user = get_user_model().objects.get(id=userId)
    emailContent = build_email_relatory(user.id)
    if not emailContent:
        return
    send_mail_task.apply_async(
        args=(
            [user.email],
            'Relatório diário de contas',
            emailContent
        )
    )

    
