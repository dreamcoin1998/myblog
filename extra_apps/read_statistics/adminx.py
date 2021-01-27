from .models import ReadNum
from django import template
import xadmin
register = template.Library()
# Register your models here.

class ReadNumAdmin:
    list_display = ('read_number', 'content_object')
    ordering = ('id',)

xadmin.site.register(ReadNum, ReadNumAdmin)
@register.filter(name='cut')
def replace(value, arg):
    return value.replace(' ', '')
