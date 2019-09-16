from django import template

register = template.Library()

@register.filter
def summa(value, choice):
    return value + choice