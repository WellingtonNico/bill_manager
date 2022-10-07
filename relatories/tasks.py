from celery import shared_task

from relatories.models import BillRelatory


@shared_task(name='process_bill_relatory')
def process_bill_relatory(id):
    obj:BillRelatory = BillRelatory.objects.get(id=id)
    obj.status = 'PROCESSING'
    obj.save()
    obj.process()
