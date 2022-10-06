from django.core.management.base import BaseCommand
from core.celery import app


class Command(BaseCommand):
    help = 'Atividades para rodar a cada semana.'

    def handle(self,*args,**kwargs):
        # limpeza da tabela das tasks
        app.signature('celery.backend_cleanup').apply_async()
        self.stdout.write('Tarefas enviadas para fila.')
