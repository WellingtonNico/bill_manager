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
        countTotal = 0
        totalValueSum = 0
        for status in ('EXPIRED','EXPIRES_TODAY','WARNING','TO_EXPIRE'):
            querySet = self.filter(status=status)
            valueSum = querySet.aggregate(Sum('value'))['value__sum']
            if not valueSum:
                valueSum = 0
            totalValueSum += valueSum
            count = querySet.count()
            countTotal += count
            data[status] = {
                'count':count,
                'value_sum':round(valueSum,2)
            }
        data['TOTAL'] = {
            'count':countTotal,
            'value_sum':round(totalValueSum,2)
        }
        return data


class BillManager(Manager):
    _queryset_class = BillQueryset


