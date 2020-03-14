from django import template

register = template.Library()

@register.filter
def times(number):
    return range(1,number+1)

@register.filter
def formQuestion(number):
    return vars()["formQuestion"+str(number)]