from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Bill
from datetime import datetime


@shared_task(name='process_user_bills')
def process_user_bills(userId):
    ''' 
    responsável por fazer o processamento de todas as contas do usuário
    que precisem ser atualizadas no dia em que a task rodar
    '''
    # primeiro ajustase DEVE filtrar por status específicos
    expiresTodayBills = Bill.objects.filter(
        user_id=userId,expiration_date=datetime.now().date()
    )
    expiresTodayBills.update(status='EXPIRES_TODAY')
    user = get_user_model.objects.get(id=userId)
