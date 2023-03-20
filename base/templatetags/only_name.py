from django import template

register = template.Library()

@register.filter(name='only_name')
def only_name(p):
    name = p.split('/')
    return name[2]

register.filter('only_name', only_name)