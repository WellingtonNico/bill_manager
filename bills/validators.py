from django.forms import ValidationError
from datetime import datetime


def only_greater_than_zero(value):
    if not int(value) > 0:
        raise ValidationError('O valor deste campo não pode ser menor ou igual a 0')


def only_positive_numbers(value):
    if not int(value) >= 0:
        raise ValidationError('O valor deste campo não pode se menor que 0')


def only_date_lower_or_equal_today(value):
    ''' 
    funciona somente para objetos do tipo date e não datetime
    '''
    if value > datetime.now().date():
        raise ValidationError('Esta dada não pode ser superior ao dia de hoje')