from django import template
from ..models import Region

register = template.Library()

@register.filter
def region_name(value):
    if value == 0:
        return ''
    region = Region.objects.get(pk=value)
    return region.name


@register.filter
def access(value):
    value = str(value).replace('[','').replace(']','').replace('\'','')
    if value == '':
        return '0'
    else:
        return value