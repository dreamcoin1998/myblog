from django.contrib import admin
from .models import ReadNum
from django import template
register = template.Library()
# Register your models here.

class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_number', 'content_object')
    ordering = ('id',)

admin.site.register(ReadNum)
@register.filter(name='cut')
def replace(value, arg):
    return value.replace(' ', '')