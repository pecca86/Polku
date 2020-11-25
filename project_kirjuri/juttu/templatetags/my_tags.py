from django import template
import datetime

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val

@register.simple_tag
def current_time():
    return datetime.datetime.now()