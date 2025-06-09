from django import template

register = template.Library()

@register.filter
def somar(lista, campo):
    return sum(getattr(obj, campo, 0) for obj in lista)