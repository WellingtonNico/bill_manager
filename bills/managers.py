from django.db.models import QuerySet,Manager,Sum


class BillQueryset(QuerySet):
    def build_relatory(self):
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
        data = {}
        for status in ('EXPIRED','EXPIRES_TODAY','WARNING','TO_EXPIRE'):
            querySet = self.filter(status=status)
            valueSum = querySet.aggregate(Sum('value'))['value__sum']
            if not valueSum:
                valueSum = 0
            data[status] = {
                'count':querySet.count(),
                'value_sum':round(valueSum,2)
            }
        return data


class BillManager(Manager):
    _queryset_class = BillQueryset


