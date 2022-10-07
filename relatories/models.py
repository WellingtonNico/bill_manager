from django.db import models
from relatories.constants import *
from users.models import User
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY
from datetime import datetime
from core.celery import app


def get_month_periods(start_month, start_year, end_month, end_year):
    start = datetime(start_year, start_month, 1)
    end = datetime(end_year, end_month, 1)
    return [(d.month, d.year) for d in rrule(MONTHLY, dtstart=start, until=end)]


class BillRelatory(models.Model):
    user:User = models.OneToOneField(User,on_delete=models.CASCADE)
    start_year = models.IntegerField(verbose_name='Ano inicial')
    end_year = models.IntegerField(verbose_name='Ano final')
    start_month = models.IntegerField(verbose_name='Mês inicial',choices=MONTHS_CHOICES)
    end_month = models.IntegerField(verbose_name='Mês final',choices=MONTHS_CHOICES)
    updated_date = models.DateTimeField(auto_now=True)
    data = models.JSONField(default=dict,blank=True,null=True)
    status = models.CharField(verbose_name='Status',max_length=12,choices=BILL_RELATORY_STATUSES,default='NEW')

    class Meta:
        verbose_name = 'Relatório de Contas'
        verbose_name_plural = 'Relatórios de Contas'

    def process(self):
        self.data = {}
        index = 0
        try:
            for month,year in get_month_periods(self.start_month,self.start_year,self.end_month,self.end_year):
                queryset = self.user.get_bills().filter(created_date__year=year,created_date__month=month)
                data = queryset.build_relatory()
                data['date'] = f"{MONTHS[month]} - {year}"
                self.data[index] = data
                index += 1 
            self.status = 'COMPLETED'
        except Exception as e:
            self.status = 'ERROR'
        self.save()

    def enqueue(self):
        app.signature('process_bill_relatory').apply_async(args=(self.id,))
        self.status = 'QUEUED'
        self.save()

    def get_period_from_to(self):
        if self.data:
            return f"{list(self.data.values())[0]['date']} até {list(self.data.values())[-1]['date']}"
        return 'informação não disponível'

    def is_empty(self) -> bool:
        return self.data == {}

    


''' 
cada objeto da lista deverá ter os campos
vencidas
vence hoje
atenção
a vencer
total : {
    count:
    value_sum:
}
'''