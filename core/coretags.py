from django import template

register = template.Library()

@register.filter(name='to_int')
def to_json(value):
    return int(value)