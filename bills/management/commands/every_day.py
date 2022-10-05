from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'tarefas que precisam rodar uma vez por dia.'

    def handle(self,*args,**kwargs):
        self.stdout.write('concluído.')