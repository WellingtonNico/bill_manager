from django.core.exceptions import ValidationError


def document_validator(value):
    if not value:
        return
    if not value.isnumeric():
        raise ValidationError('o campo deve conter apenas números')
    if len(str(value)) > 14:
        raise ValidationError('o campo pode ter até 14 números somente')