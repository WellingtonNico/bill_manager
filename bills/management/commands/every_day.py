from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from bills.tasks import process_user_bills


class Command(BaseCommand):
    help = 'tarefas que precisam rodar uma vez por dia.'

    def handle(self,*args,**kwargs):
        for user in get_user_model().objects.all().iterator():
            process_user_bills.apply_async(args=(user.id,))

        self.stdout.write('concluído.')