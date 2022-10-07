from django import template
from django.utils.safestring import mark_safe


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

