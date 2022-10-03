import os
from celery import Celery
from django.conf import settings
from celery.signals import worker_init

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


app = Celery('core.celery')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

def restoreStarted():
    app.connection().channel().qos.restore_visible()

@worker_init.connect
def restore(sender=None,conf=None,**kwargs):
    restoreStarted()

# filas usadas para o celery
REAL_TIME_QUEUE = settings.QUEUES[0]
FAST_TASK_QUEUE = settings.QUEUES[1]
HEAVY_TASKS_QUEUE = settings.QUEUES[2]


# níveis de prioridade para o celery
XXL = 0
XL = 1
L = 2
MD = 3
H = 4
XH = 5