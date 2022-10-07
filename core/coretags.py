from django import template
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

register = template.Library()

@register.filter(name='to_int')
def to_json(value):
    return int(value)


@register.filter(name='build_params')
def build_params(request):
    newUrl = ''
    for key,value in request.GET.items():
        if key != 'page' and value:
            newUrl += f'{key}={value}&'

    return newUrl


@register.filter(name='to_currency')
def to_currency(value):
    return locale.currency(value,grouping=True,symbol=False)


