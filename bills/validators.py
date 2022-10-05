from django.forms import ValidationError
from datetime import datetime
from django.conf import settings
from django.db.models import FileField


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


def payment_proof_file_size_validator(value):
    if len(value) > settings.PAYMENT_PROOFS_MAX_LENGTH_KB * 1024:
        raise ValidationError(f'O tamanho do arquivo excede o tamanho máximo permitido de {settings.PAYMENT_PROOFS_MAX_LENGTH_KB}KB')


def payment_proof_file_format_validator(value):
    if hasattr(value.file,'content_type'):
        if not 'image' in value.file.content_type and not 'pdf' in value.file.content_type:
            raise ValidationError('Formato de arquivo não permitido, são permitidos somente PDF e imagens')

