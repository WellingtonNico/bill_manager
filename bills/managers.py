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
            data[status] = {
                'count':querySet.count(),
                'value_sum':float(querySet.aggregate(Sum('value'))['value_sum'])
            }
        return data


class BillManager(Manager):
    _queryset_class = BillQueryset


